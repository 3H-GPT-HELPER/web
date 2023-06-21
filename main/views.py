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
    
    
    #생각해보니 다 필요없고 proxy에서 받은 data user db에 넣은 후 
    #그거 보여주게 html짜면됨
    
    # if 'hey' in request.session:
    #     data = request.session['hey']
    #     print("없냐?")
    #     print(data)
    #     del request.session['hey']  # 데이터 사용 후 세션에서 제거
    #     return render(request, 'main/main.html', {'data': data})
    # data = request.GET.get('data')
    # if data:
    #     print("proxy 에서 받음:", data)
    #     request.session['hey'] = data  # 세션에 데이터 저장
    #     datas=data
    
    return render(request, 'main/main.html',context=context)


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
            
            topic = preprocessing(answer_str)
            #print(topic)
            
            content.keywords = topic
            content.save()
            #print(type(content))
            
            #print(pd.DataFrame.from_records(answer_str))

        except json.JSONDecodeError:
            return HttpResponseBadRequest('invalid json data')
        
        
        print("main으로 보내버려~")
        # request.session.modified = True #세션 삭제 가능하도록 등록
        # request.session['hey']=answer
 
        #return render(request,'main/main.html',{'data':answer})
        # main 함수로 리디렉션
        #return HttpResponseRedirect(reverse('main'))
        
         # main 함수로 리디렉션할 URL 생성
        # url = reverse('main') + '?data=' + answer

        # # main 함수로 리디렉션
        # return HttpResponseRedirect(url)
        
        #다 필요없고 user db에 추가하는 코드


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
    keywords= '/'.join(topic)
    
    return keywords
    
    
    
    
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