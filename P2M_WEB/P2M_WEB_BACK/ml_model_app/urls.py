from django.urls import path, include
from . import views


urlpatterns = [   
    path('api/predict/', views.predict, name='api_predict'),
]
