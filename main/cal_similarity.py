#pip install promcse
#from promcse import PromCSE
import joblib
from django.contrib.auth.models import User
from user.models import UserCategory 
from main.models import Content
import numpy as np
from numpy import dot
from numpy.linalg import norm
from .extract_topic import *
import torch
from .apps import *


#받은 쿼리와 기존의 토픽들 간 거리 비교
def cal_similarity(request, answer_str):
    THRESHOLD = 0.8
    #userCategories=UserCategory.objects.filter(user_id__user_id=request.user.user_id)
    print(request.user.username)
    categories = []
    answers = []
    #userCategories=UserCategory.objects.filter(user_id__username=request.user.username).values_list('inserted_category')
    userCategories=UserCategory.objects.filter(user_id__username=request.user.username)
    userAnswers = Content.objects.filter(user_id__username = request.user.username)
    for u in userCategories:
        categories.append(u.inserted_category)
        
    #for a in userAnswers:
    #    answers.append(a.answer)
        
    scores = [] #dictionary
    print("******")
    print("django usercategories list: ", categories)
    print("******")
    #categories = list(userCategories) #userCategories의 카테고리 값들만 들어있는 리스트
    
    #만약 비어 있으면 바로 리턴
    if len(categories) == 0 or len(userAnswers) == 0:
        return {'new': answer_str}
        
    scores = ModelConfig.test_model.similarity(answer_str,categories)
    #print("scores:",scores)

    '''
    #시간이 너무 오래 걸릴 경우 -> 대표 토픽과의 거리만 측정하기
    for a in userAnswers:
        topics = extract_topic(a.answer)
        topic_arr = topics.split("/")
        score3 = []
        for t in topic_arr:
            score = ModelConfig.model.similarity(answer_str,t)
            score3.append(score)
        scores.append(score3)
    '''
    # 기존 category에 내용 추가
    
    #print("max scores: ", max(map(max,scores)))
    print("max_score:",max(scores))
    
    #max_score = max(map(max,scores))
    max_score = max(scores)
    
    if max_score >= THRESHOLD:
        #print(scores.index(max(scores)))
        #ij=[(i,j) for i in range(len(scores)) for j in range(len(scores[0])) if scores[i][j]==max_score]
        #print(ij)
        #category = categories[ij[0][0]]
        ii = list(scores).index(max_score)
        category = categories[ii]
        print("{existed':", category,"}")
        return {'existed': category}
    # 새로운 category 생성
    else:
        print("{new':", answer_str,"}")
        return {'new': answer_str}
