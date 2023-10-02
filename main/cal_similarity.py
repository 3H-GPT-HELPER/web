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

#model = joblib.load('/Users/hgy/Desktop/promcse_model.pkl')

from promcse import PromCSE

model_name_or_path = 'YuxinJiang/unsup-promcse-bert-base-uncased'
pooler_type = 'cls_before_pooler'
pre_seq_len = 16

model = PromCSE(model_name_or_path=model_name_or_path, 
          pooler_type=pooler_type,
          pre_seq_len=pre_seq_len)

def cos_similarity(a,b):
    return dot(a,b)/(norm(a)*norm(b))


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
    if len(categories) == 0 :
        return {'new': answer_str}
    
    #for category in categories:
    #    #category랑 answer_str 거리값 계산
    #    score = model.similarity(answer_str,category)
    #    scores.append(score)
        
    #for answer in answers:
    #    score = model.similarity(answer_str, answer)
    #    scores.append(score)
    
    for a in userAnswers:
        topics = extract_topic(a.answer)
        topic_arr = topics.split("/")
        score3 = []
        for t in topic_arr:
            score = model.similarity(answer_str,t)
            score3.append(score)
        scores.append(score3)
    
    '''
    model.build_index(userCategories, use_faiss=False)
    results = model.search(answer_str)
    for i, result in enumerate(results):
        print("Retrieval results for query: {}".format(answer_str[i]))
        for sentence, score in result:
            print("    {}  (cosine similarity: {:.4f})".format(sentence, score))
            scores.add(score)
        print("")
        
    '''
    
    # 기존 category에 내용 추가
    
    print("max scores: ", max(map(max,scores)))
    
    if max(map(max,scores)) >= THRESHOLD:
        #print(scores.index(max(scores)))
        ij=[(i,j) for i in range(len(scores)) for j in range(len(scores[0])) if scores[i][j]==1]
        category = userAnswers[ij[0]].inserted_category
        print("{existed':", category,"}")
        return {'existed': category}
    # 새로운 category 생성
    else:
        print("{new':", answer_str,"}")
        return {'new': answer_str}
