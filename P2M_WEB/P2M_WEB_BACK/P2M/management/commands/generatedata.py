# In generate_test_data.py

from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
from faker import Faker
from random import uniform
from P2M.models import Mesure, Sensor

class Command(BaseCommand):
    help = 'Generates test data for the Mesure model'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get the sensor with id = 000000000000000000000001
        sensor = Sensor.objects.get(id='000000000000000000000001')

        # Generate test data for each day from 19-03-2023 to 18-03-2024
        start_date = datetime(2023, 3, 19)
        end_date = datetime(2024, 3, 18)
        current_date = start_date

        while current_date <= end_date:
            Mesure.objects.create(
                date=current_date,
                ph=uniform(50, 150),
                temperature=uniform(50, 150),
                humidity=uniform(50, 150),
                nitrogen=uniform(50, 150),
                phosphorus=uniform(50, 150),
                potassium=uniform(50, 150),
                rainfall=uniform(50, 150),
                sensor=sensor,
                sensor_latitude=36.870142,
                sensor_longitude=10.167193
            )
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Test data generated successfully'))
