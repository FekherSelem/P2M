from django.shortcuts import render,redirect
from .models import Sensor, Mesure
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import MesureSerializer
import numpy as np
from django.apps import apps
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
from rest_framework.parsers import JSONParser


# Create your views here.

def home(request):

    return render(request,'P2M/Home.html')
def about(request):
    context={
        'title':'About'
    }
    return render(request,'P2M/About.html', context)
@method_decorator(login_required, name='dispatch')
class SensorListView(ListView):
    model = Sensor
    context_object_name = 'sensors'

    def get_queryset(self):
        return Sensor.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensors_data = list(self.get_queryset().values('id', 'name', 'latitude', 'longitude'))
        context['sensors_json'] = json.dumps(sensors_data)
        return context

@method_decorator(login_required, name='dispatch')
class SensorDetailView(DetailView):
    model = Sensor

    def dispatch(self, request, *args, **kwargs):
        # Get the sensor object
        self.sensor = self.get_object()

        # Check if the sensor belongs to the current user
        if self.sensor.user != request.user:
            messages.warning(request, f'This is not your sensor! choose one of your own.')
            return redirect ('sensors')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensor = self.get_object()
        
        # Filter the Mesure objects based on the same longitude and latitude as the sensor
        mesure_list = list(Mesure.objects.filter(
            sensor_latitude=sensor.latitude,
            sensor_longitude=sensor.longitude
        ).values(
            'id', 'date', 'ph', 'temperature', 'humidity', 'nitrogen', 'phosphorus', 
            'potassium', 'rainfall', 'sensor_latitude', 'sensor_longitude'
        ))
        
        # Convert datetime objects to string representations
        for mesure in mesure_list:
            mesure['date'] = mesure['date'].strftime('%Y-%m-%d %H:%M:%S')
        
        context['mesure_json'] = json.dumps(mesure_list, cls=DjangoJSONEncoder)
        return context

@method_decorator(login_required, name='dispatch')
class SensorCreateView(CreateView):
    model = Sensor
    fields = ['id','name','latitude','longitude']

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('sensors')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emptylist =[]
        context['sensor_json'] = json.dumps(emptylist)
        return context
    
@method_decorator(login_required, name='dispatch')
class SensorUpdateView(UpdateView):
    model = Sensor
    fields = ['id','name','latitude','longitude']

    def dispatch(self, request, *args, **kwargs):
        # Get the sensor object
        self.sensor = self.get_object()

        # Check if the sensor belongs to the current user
        if self.sensor.user != request.user:
            messages.warning(request, f'This is not your sensor! choose one of your own.')
            return redirect ('sensors')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('sensors')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sensor_data = {
            'id': self.object.id,
            'name': self.object.name,
            'latitude': self.object.latitude,
            'longitude': self.object.longitude,
        }
        context['sensor_json'] = json.dumps(sensor_data)
        return context

@method_decorator(login_required, name='dispatch')
class SensorDeleteView(DeleteView):
    model = Sensor

    def dispatch(self, request, *args, **kwargs):
        # Get the sensor object
        self.sensor = self.get_object()

        # Check if the sensor belongs to the current user
        if self.sensor.user != request.user:
            messages.warning(request, f'This is not your sensor! choose one of your own.')
            return redirect ('sensors')
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse_lazy('sensors')

@api_view(['POST'])
def create_mesure(request):
    # {
    # "ph": 7,
    # "temperature": 24,
    # "humidity": 100,
    # "nitrogen": 101,
    # "phosphorus": 102,
    # "potassium": 103,
    # "rainfall": 105,
    # "sensor": "000000000000000000000003"
    # }

    # Extract sensor ID from request data
    sensor_id = request.data.get('sensor')
    
    # Lookup the Sensor object based on the provided ID
    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        return Response({"error": "Sensor does not exist fekher"}, status=status.HTTP_400_BAD_REQUEST)

    # Extract latitude and longitude from the retrieved Sensor object
    
    latitude = sensor.latitude
    longitude = sensor.longitude

    # Set the sensor_latitude and sensor_longitude fields in request data
    request.data['sensor'] = sensor.id
    request.data['sensor_latitude'] = latitude
    request.data['sensor_longitude'] = longitude

    serializer = MesureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


