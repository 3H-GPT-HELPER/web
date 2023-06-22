from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest,HttpResponseRedirect
from django.middleware.csrf import get_token


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http.request import HttpRequest

from .models import Content
from user.models import UserKeywords

#pip install nltk, scikit-learn, pandas 필요
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 

import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import numpy as np

def index(request):
    return render(request,'main/index.html')

def signup(request):
    return render(request,"main/signup.html")

def login(request):
    return render(request, 'main/login.html')

def main(request):
    print("this is main page")
    
    userContents=Content.objects.filter(userName="hw")
    context={'contents':userContents}
    #preprocessing(userContents)
    
    return render(request, 'main/main.html',context=context)

def category(request):
    userkeywords=UserKeywords.objects.filter(user_id__name='hw')
    context={'userkeywords':userkeywords}
    
    #우선 여기에 topic 과 category 매칭 코드 구현:return값 해당 category_id
    #content의 topcisd와 userkeywords의 name을 비교하면됨 그 후 select된 걸 content.category로 지정
    #index=content.objects.filter(category__serKeywords_id)로 번호 할당받기
    #index별로 detail페이지 생성

    #전달받은 top topic 3개 리스트와 UserKeywords.name 중 동일한거 match 후 그 유저키워드.네임을 content.category로 지정 이거 초반에 content.save할때완료



    
    

    return render(request,"main/category.html",context=context)

def category_detail(request,category_id):

    #usesrkeywords.name이랑 content.category랑 같으면 그 content들을 가져와서 보낸다.
    #userkeywords.id를 페이지 id로 넘긴다

    #category 1
    uk=UserKeywords.objects.get(userKeywords_id=category_id)
    
    uk_name=uk.name
    category_id=uk.userKeywords_id
    userContents=Content.objects.filter(category=uk_name)
    context={'contents':userContents,'category_id':category_id}
    #category 2

    #category_id와 동일하게 분류된 content를 filter 그 contents던지기
    #userContents=Content.objects.filter(userName="hw")
    
    #category->userKeywords_id를 받은거로 detail 페이지 생성

    return render(request,'main/detail.html',context=context)


@csrf_exempt
def proxy(request):
    if request.method == 'POST':    
        try:
            data=json.loads(request.body.decode('utf-8'))
            answer=data['data']
            #answer=answer[0]
            print("!!!!!!!!!!!!!!!!!!!!!!")
            print(type(answer))
            
            answer_str = ''.join(answer)
            print(answer_str)
            
            #entity 생성 
            content=Content(answer=answer_str)
            
            topics = preprocessing(answer_str)
            #print(topic)
            
            topic_arr = topics.split("/")
            content.topics = topics

            
            category=get_category(topic_arr)
            print(category)
            content.category=category

            content.save()
            #print(type(content))


        except json.JSONDecodeError:
            return HttpResponseBadRequest('invalid json data')
        
        
        print("main으로 보내버려~")
       

    return JsonResponse({'error': 'Invalid request method'})

def preprocessing(answer):
    #print(context['contents'])
    
    data = pd.DataFrame({'answer':[answer]})
    #context = context['contents']
    #print(context['contents'])
    data['answer'] = data.apply(lambda row: nltk.word_tokenize(row['answer']),axis=1)
    print(data)
    stop_words_list = stopwords.words('english')
    tokenized = data['answer'].apply(lambda x: [word for word in x if len(word) > 2])
    detokenized = []
    for i in range(len(data)):
        t = ' '.join(tokenized[i])
        detokenized.append(t)
    context = detokenized
    vectorizer = TfidfVectorizer(stop_words='english',max_features=10)
    X = vectorizer.fit_transform(context)
    
    lda_model = LatentDirichletAllocation(n_components=1, learning_method='online', random_state=777, max_iter=3)
    lda_top = lda_model.fit_transform(X)
    
    topic = get_topics(lda_model.components_,vectorizer.get_feature_names_out())
    #print('/'.join(topic))
    topics= '/'.join(topic)
    
    return topics
    
    
    
    
def get_topics(components, feature_names, n=3):
    topic = []
    
    '''
    for idx, topic in enumerate(components):
        print("Topic %d:" % (idx+1),[(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])
        #for i in topic.argsort()[:-n - 1:-1] :
            #print("Topic %d:" % (idx+1),[(feature_names[i], topic[i].round(2)) ])
            #topic += feature_names[i]
    '''
    for idx, topic in enumerate(components):
       # top_features = [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]]
       top_features = [feature_names[i] for i in topic.argsort()[:-n - 1:-1]]

    print(top_features)
        
    return top_features

#둘다 리스트로 보내서 돌려봐요,,
def get_category(top_features):
    selected_category=""
    userkeywords_set=UserKeywords.objects.filter(user_id__name='hw')
    uk_list=[]
    for k in userkeywords_set:
        uk_list.append(k.name)

    print("???")
    print(top_features,uk_list)

    for item in top_features:
        if item in uk_list:
            selected_category=item
    
    return selected_category

