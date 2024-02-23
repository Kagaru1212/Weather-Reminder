from rest_framework import serializers

from weather.models import Subscribing


class WeatherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    city_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Subscribing
        fields = ('user', 'city_name', 'notification')

    def create(self, validated_data):
        """
        This method allows you to automatically populate the user field with the name of the registered user.
        """
        user = self.context['request'].user
        subscribing_instance = Subscribing(user=user, **validated_data)
        subscribing_instance.save()
        return subscribing_instance

    def update(self, instance, validated_data):
        instance.notification = validated_data.get('notification', instance.notification)
        instance.city_name = validated_data.get('city_name', instance.city_name)
        instance.save()
        return instance
