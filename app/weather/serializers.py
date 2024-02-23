import requests
from rest_framework import serializers

from weather.models import Subscribing
from weather.tasks import send_weather
import logging

logger = logging.getLogger(__name__)


class WeatherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    city_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Subscribing
        fields = ('user', 'city_name', 'notification')

    def create(self, validated_data):
        user = self.context['request'].user
        city_name = validated_data.get('city_name')

        # Проверка наличия города в стороннем API
        if self.is_valid_city(city_name):
            subscribing_instance = Subscribing(user=user, **validated_data)
            subscribing_instance.save()

            send_weather.delay(user.email, city_name)

            logger.info(f'Sending weather task for user {user.email} and city {city_name}')

            return subscribing_instance
        else:
            raise serializers.ValidationError({'city_name': 'City not found in the external API'})

    def update(self, instance, validated_data):
        instance.notification = validated_data.get('notification', instance.notification)
        instance.city_name = validated_data.get('city_name', instance.city_name)
        instance.save()
        return instance

    def is_valid_city(self, city_name):
        appid = '6dabbdf16a4a011fc0e41ae5cb097de4'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={appid}'

        response = requests.get(url)
        return response.status_code == 200
