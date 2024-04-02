from django.urls import path, include
from . import views
from .views import predict


urlpatterns = [
    path('predict/', views.predict, name='predict'),
   
    path('api/predict/', views.predict, name='api_predict'),
]
