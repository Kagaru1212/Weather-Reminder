import json

import requests
from rest_framework import serializers

from weather.models import Subscribing
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class WeatherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    city_name = serializers.CharField(max_length=255, required=False)
    notification = serializers.IntegerField()

    class Meta:
        model = Subscribing
        fields = ('user', 'city_name', 'notification')

    def create(self, validated_data):
        user = self.context['request'].user
        city_name = validated_data.get('city_name')
        notification = int(validated_data.get('notification', ''))

        # Checking the availability of a city in a third-party API
        if self.is_valid_city(city_name):
            subscribing_instance = Subscribing(user=user, **validated_data)
            subscribing_instance.save()

            if notification == 3:
                schedule = IntervalSchedule.objects.create(every=180, period=IntervalSchedule.SECONDS)
            elif notification == 6:
                schedule = IntervalSchedule.objects.create(every=360, period=IntervalSchedule.SECONDS)
            else:
                schedule = IntervalSchedule.objects.create(every=720, period=IntervalSchedule.SECONDS)

            PeriodicTask.objects.create(
                interval=schedule,
                name=f'{user}_task_{city_name}',
                task='weather.tasks.send_weather',
                args=json.dumps([user.email, city_name])
            )

            return subscribing_instance
        else:
            raise serializers.ValidationError({'city_name': 'City not found in the external API'})

    def update(self, instance, validated_data):
        instance.notification = validated_data.get('notification', instance.notification)
        instance.city_name = validated_data.get('city_name', instance.city_name)
        instance.save()

        if instance.notification == 3:
            schedule = IntervalSchedule.objects.create(every=180, period=IntervalSchedule.SECONDS)
        elif instance.notification == 6:
            schedule = IntervalSchedule.objects.create(every=360, period=IntervalSchedule.SECONDS)
        else:
            schedule = IntervalSchedule.objects.create(every=720, period=IntervalSchedule.SECONDS)

        # Getting a periodic task by username and city name
        periodic_task = PeriodicTask.objects.get(name=f'{instance.user}_task_{instance.city_name}')

        # Updating the interval of a periodic task
        periodic_task.interval = schedule
        periodic_task.save()
        return instance

    def is_valid_city(self, city_name):
        appid = '6dabbdf16a4a011fc0e41ae5cb097de4'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={appid}'

        response = requests.get(url)
        return response.status_code == 200

    def validate_notification(self, value):
        if value not in [3, 6, 12]:
            raise serializers.ValidationError("Notification value should be 3, 6, or 12")
        return value
