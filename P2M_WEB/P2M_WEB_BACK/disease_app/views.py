from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .apps import DiseaseAppConfig
import numpy as np
from django.apps import apps
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import io

@api_view(['POST'])
def predict_disease(request):
    # Get the model from the app config
    model_app_config = apps.get_app_config('disease_app')
    model = model_app_config.model
    disease_classes = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']


    if request.method == 'POST':
        if 'image' not in request.FILES:
            return Response({'error': 'Image file not provided'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        try:
            image = Image.open(image_file)
            image = image.resize((64, 64))  # Resize the image to the expected dimensions
            image_array = np.asarray(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
            
            prediction = model.predict(image_array)
            predicted_index = np.argmax(prediction[0])
            predicted_disease = disease_classes[predicted_index]
            return Response({'prediction': predicted_disease})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
