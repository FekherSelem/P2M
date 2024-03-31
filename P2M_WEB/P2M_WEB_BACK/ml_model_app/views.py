from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .apps import MlModelAppConfig
import numpy as np

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            data = request.POST.get('data')
            # Assuming 'data' is a list of features, you might need to adjust parsing based on your input format
            features = np.array([float(num) for num in data.split(',')])
            prediction = MlModelAppConfig.model.predict([features])
            return JsonResponse({'prediction': prediction.tolist()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Send a POST request with valid parameters'})
