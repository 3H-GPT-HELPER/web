from django.apps import AppConfig
from promcse import PromCSE
import joblib


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

class ModelConfig(AppConfig):
    test_model = joblib.load(r'/Users/hgy/Desktop/model.pkl')
    #huda: C:\Users\nrul\Downloads\model.pkl
    #hw: /Users/ohbom/Downloads/model.pkl