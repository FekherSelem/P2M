from django.apps import AppConfig
import joblib
import os

relative_model_path = "../../../P2M_ML/python_crop_recommendation/model_pipeline_nb.joblib"
script_directory = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.normpath(os.path.join(script_directory, relative_model_path))


class MlModelAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_model_app'
    model = None  # Placeholder for the loaded model

    def ready(self):
        
        # Load your model
        if not self.model:
            self.model = joblib.load(model_file_path)
        


