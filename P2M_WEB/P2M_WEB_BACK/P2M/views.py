from django.shortcuts import render,redirect
from .models import Sensor, Mesure
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy

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
            sensor__latitude=sensor.latitude,
            sensor__longitude=sensor.longitude
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