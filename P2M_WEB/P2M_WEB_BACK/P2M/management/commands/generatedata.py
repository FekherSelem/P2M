from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from faker import Faker
from random import gauss, uniform
from P2M.models import Mesure, Sensor
import numpy as np

class Command(BaseCommand):
    help = 'Generates test data for the Mesure model'

    def simulate_seasonal_temperature(self, current_date, start_date, end_date):
        """Simulates seasonal variation in temperature."""
        # Calculate the fraction of the way through the period
        year_fraction = (current_date - start_date).days / (end_date - start_date).days
        # Temperature varies sinusoidally through the year
        mid_range_temp = 15  # Average mid-range temperature
        amplitude = 20  # Difference between peak summer and deep winter
        seasonal_variation = amplitude * np.sin(np.pi * 2 * year_fraction)
        return mid_range_temp + seasonal_variation + gauss(0, 5)  # Adding random daily fluctuation

    def handle(self, *args, **kwargs):
        fake = Faker()

        sensor = Sensor.objects.get(id='000000000000000000000004')

        start_date = datetime(2023, 4, 2)
        end_date = datetime(2024, 4, 2)
        current_date = start_date

        while current_date <= end_date:
            Mesure.objects.create(
                date=current_date,
                ph=uniform(0, 14),  # More realistic pH range
                temperature=self.simulate_seasonal_temperature(current_date, start_date, end_date),
                humidity=uniform(0, 100),
                nitrogen=uniform(0, 150),
                phosphorus=uniform(0, 150),
                potassium=uniform(0, 150),
                rainfall=uniform(0, 300),
                sensor=sensor,
                sensor_latitude=	36.890482,
                sensor_longitude=10.183483,
            )
            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS('Test data generated successfully'))










