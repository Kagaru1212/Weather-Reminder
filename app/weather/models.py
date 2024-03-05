from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask
from django.db import models
from django.contrib.auth import get_user_model


class Subscribing(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    city_name = models.CharField(max_length=255)
    notification = models.IntegerField(blank=True)

    objects = models.Manager()

@receiver(pre_delete, sender=Subscribing)
def delete_periodic_task(sender, instance, **kwargs):
    try:
        periodic_task = PeriodicTask.objects.get(name=f'{instance.user}_task_{instance.city_name}')
        periodic_task.delete()
    except PeriodicTask.DoesNotExist:
        pass