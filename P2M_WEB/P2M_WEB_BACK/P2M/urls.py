from django.urls import path
from . import views
from .views import SensorListView, SensorDetailView, SensorCreateView,SensorUpdateView,SensorDeleteView,create_mesure

urlpatterns = [
    path('', views.home, name='P2M-home'),
    path('sensors_list/', SensorListView.as_view(), name='sensors'),
    path('sensor/new/', SensorCreateView.as_view(), name='sensor-create'),
    path('sensor/<pk>/', SensorDetailView.as_view(), name='sensor-detail'),
    path('sensor/<pk>/update/', SensorUpdateView.as_view(), name='sensor-update'),
    path('sensor/<pk>/delete/', SensorDeleteView.as_view(), name='sensor-delete'),
    path('mesures/', create_mesure, name='create_mesure'),
    path('predict/', views.predict, name='predict'),
    path('about/', views.about, name='P2M-about'),
    
]
