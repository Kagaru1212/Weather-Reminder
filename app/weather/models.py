import redis
from django.contrib.auth import get_user_model
from django.db import models


class Subscribing(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    notification = models.IntegerField(blank=True)

    objects = models.Manager()

    def save_weather_to_redis(self, city_name, weather_data):
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        key = f'city_weather:{city_name}'
        redis_client.set(key, weather_data)
