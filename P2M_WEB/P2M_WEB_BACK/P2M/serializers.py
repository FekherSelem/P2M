# serializers.py
from rest_framework import serializers
from .models import Mesure

class MesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesure
        fields = ['ph', 'temperature', 'humidity', 'nitrogen', 'phosphorus', 'potassium', 'rainfall', 'sensor', 'sensor_latitude', 'sensor_longitude']

    # You can also include validation logic here if needed
