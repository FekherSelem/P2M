from django.apps import AppConfig
import keras
import os

relative_model_path = "../../../P2M_ML/python_crop_disease/final_model.keras"
script_directory = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.normpath(os.path.join(script_directory, relative_model_path))


class DiseaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'disease_app'
    model = None  # Placeholder for the loaded model

    def ready(self):
        
        # Load your model
        if not self.model:
            self.model = keras.models.load_model(model_file_path)
        


