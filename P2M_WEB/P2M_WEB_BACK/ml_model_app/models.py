from django.apps import AppConfig
import joblib

class MlModelAppConfig(AppConfig):
    name = 'ml_model_app'
    model = None

    def ready(self):
        # Load your model here
        self.model = joblib.load('ml_model_app/models/model_pipeline_nb.joblib')
