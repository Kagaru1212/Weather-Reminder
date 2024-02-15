from rest_framework import serializers

from weather.models import Subscribing


class WeatherSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Subscribing
        fields = ('user', 'city_name', 'notification')
