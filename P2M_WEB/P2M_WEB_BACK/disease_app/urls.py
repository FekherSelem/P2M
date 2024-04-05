from django.urls import path, include
from . import views


urlpatterns = [   
    path('disease/predict_disease/', views.predict_disease, name='predict_disease'),
]
