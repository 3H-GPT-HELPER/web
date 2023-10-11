from django.apps import AppConfig
from promcse import PromCSE
import joblib


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"

class ModelConfig(AppConfig):
    #model_name_or_path = 'YuxinJiang/unsup-promcse-bert-base-uncased'
    #pooler_type = 'cls_before_pooler'
    #pre_seq_len = 16

    #model = PromCSE(model_name_or_path=model_name_or_path, 
    #      pooler_type=pooler_type,
    #      pre_seq_len=pre_seq_len)
    
    test_model = joblib.load('/Users/hgy/Downloads/model.pkl')