from django.apps import AppConfig
import joblib


class MlModelAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_model_app'
    model = None  # Placeholder for the loaded model

    def ready(self):
        
        # Load your model
        if not self.model:
            self.model = joblib.load(r'C:\Users\safag\P2M\P2M_ML\python\model_pipeline_nb.joblib')
        


