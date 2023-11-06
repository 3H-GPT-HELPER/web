import joblib
from django.contrib.auth.models import User
from user.models import UserCategory 
from main.models import Content
import numpy as np
from .extract_topic import *
import torch
from .apps import *


def cal_similarity(request, answer_str):
    THRESHOLD = 0.8
    print(request.user.username)
    categories = []
    userCategories=UserCategory.objects.filter(user_id__username=request.user.username)
    userAnswers = Content.objects.filter(user_id__username = request.user.username)
    for u in userCategories:
        categories.append(u.inserted_category)
        
    scores = [] #dictionary
    print("******")
    print("django usercategories list: ", categories)
    print("******")
    
    if len(categories) == 0 or len(userAnswers) == 0:
        return {'new': answer_str}
        
    scores = ModelConfig.test_model.similarity(answer_str,categories)
    print("max_score:",max(scores))
    
    max_score = max(scores)
    
    if max_score >= THRESHOLD:
        ii = list(scores).index(max_score)
        category = categories[ii]
        print("{existed':", category,"}")
        return {'existed': category}
    else:
        print("{new':", answer_str,"}")
        return {'new': answer_str}
