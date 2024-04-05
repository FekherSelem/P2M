from django.apps import AppConfig
import keras

class DiseaseAppConfig(AppConfig):
    name = 'disease_app'
    model = None

    def ready(self):
        # Load your model here
        self.model = keras.models.load_model('disease_app/models/final_model.keras')
