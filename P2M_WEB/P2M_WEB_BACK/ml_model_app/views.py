from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .apps import MlModelAppConfig
import numpy as np
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def predict(request):
    # Get the model from the app config
    model_app_config = apps.get_app_config('ml_model_app')
    model = model_app_config.model

    # Ensure that there is a POST request
    if request.method == 'POST':
        try:
            # Deserialize the incoming JSON data
            data = request.data
            nitrogen=data.get('Nitrogen')
            phosphorus=data.get('phosphorus')
            potassium=data.get('potassium')
            temperature = data.get('temperature')
            humidity=data.get('humidity')
            ph = data.get('ph')
            rainfall = data.get('rainfall')
            
            features=[nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall]
            
            # Assuming 'features' key in the data contains the list of features
            features = np.array(features).reshape(1,-1)
            
            # Perform prediction
            prediction = model.predict(features)
            
            # Respond with the prediction result
            return Response({'prediction': prediction[0]})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
