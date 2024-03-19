from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Sensor(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    name = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Mesure(models.Model):
    date = models.DateTimeField(default=timezone.now)
    ph = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    rainfall = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True)
    sensor_latitude = models.FloatField(null=True)
    sensor_longitude = models.FloatField(null=True)

    def __str__(self):
        return f"Measurements for {self.sensor.name} by {self.sensor.user.username} at {self.date}"