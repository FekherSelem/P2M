import os
import pickle
from django.conf import settings

def load_model():
    # Construct the full path to the pickle file within the static directory
    static_path = os.path.join(settings.BASE_DIR, 'P2M/static/P2M/CropRecommender.pkl')
    
    # Load the model from the pickle file
    with open(static_path, 'rb') as file:
        model = pickle.load(file)
    
    return model

# Load the model
model = load_model()
