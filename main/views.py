from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest,HttpResponseRedirect
from django.middleware.csrf import get_token
from httpx import Auth
from .forms import SignupForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http.request import HttpRequest
from .models import Content
from user.models import UserCategory,Users
#pip install nltk, scikit-learn, pandas, konlpy 필요
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 

import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

#from konlpy.tag import Okt

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import numpy as np
import sys
#sys.path.append('/Users/hgy/Desktop/hgy/EWHA/2023_1(4)/Final_project/3H/main')
from .cal_similarity import cal_similarity
from django.contrib.auth.models import User
from .extract_topic import *

fullanswer_str=""
answer_str=""

def signup(request: HttpRequest, *args, **kwargs):
    if request.method=='POST':
        form = SignupForm(request.POST)

        username = request.POST.get('username')
        userEmail=request.POST.get('email')
        password = request.POST.get('password2')

        print(username,userEmail,password)

        user2=Users(username=username,
                        email=userEmail,
                        password=password)
        
        user2.save()

        if form.is_valid():
            user=form.save()
            user2=Users(username=username,
                        email=userEmail,
                        password=password)
            user.save()
            user2.save()

            #auth_login(request,user)
            return redirect('/')
    
    else:
        form=SignupForm()
    return render(request,"main/signup2.html",{"form":form})


# def login(request):
#     return render(request, 'main/login2.html')

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
@csrf_exempt
def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            return redirect('user:login_success')
    else:

        form = AuthenticationForm()

    context = {
        'form': form

    }

    return render(request, 'main/login2.html', context)

from django.contrib.auth import logout as auth_logout
def logout(request):
    auth_logout(request)

    return render(request,'user/logout_success.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def main(request):
    print("this is main page")
    
    userContents=Content.objects.filter(userName="hw")
    context={'contents':userContents}
    #preprocessing(userContents)

    
    return render(request, 'main/main.html',context=context)

def category(request):
    #userCategories=UserCategory.objects.filter(user_id__user_id=request.user.user_id)
    userCategories=UserCategory.objects.filter(user_id__username=request.user.username)

    print("category!!!",request.user.username) #잘 나옴
    context={'userCategories':userCategories}
   
    return render(request,"main/category.html",context=context)

def category_detail(request,pk):
    print("category_detail!!!",request.user.username) #잘 나옴
    print("pk",pk)

    #category_id는 자동생성 및 전달되는 pk
    uc=UserCategory.objects.get(id=pk,user_id__username=request.user.username)
    print('uc: ', uc.inserted_category)
    uc_name=uc.inserted_category
    category_id=pk

    print(uc_name,category_id)
    userContents=Content.objects.filter(inserted_category__inserted_category=uc_name)
    context={'contents':userContents,'category_id':category_id}

    return render(request,'main/detail.html',context=context)

@csrf_exempt
def proxy(request):
    if request.method == 'POST':    
        try:
            data=json.loads(request.body.decode('utf-8'))
            answer=data['pTagContents']
            full_answer=data['complexContents']

            global fullanswer_str
            global answer_str
            
            answer_str = ''.join(answer) #text만 있는 답변
            fullanswer_str='new'
            fullanswer_str += ''.join(full_answer) #코드까지 합쳐진 답변
            #request.session['received_data'] = fullanswer_str
            print("?!",request.user.username)
            print("160answer_str: ", answer_str) #잘 나옴

            # new_request = HttpRequest()
            # new_request.method = 'GET'

            #add_contents(new_request,fullanswer_str)
           

        except json.JSONDecodeError:
            return HttpResponseBadRequest('invalid json data')
        
        
        print("main으로 보내버려~")

    return JsonResponse({'error': 'Invalid request method'})

def index(request):
    # users = User.objects.all()

    # for user in users:
    #     print(user.email)
    print("user test1:",request.user.username)

    global fullanswer_str
    global answer_str

    print("206answer_str: ", answer_str)

    if fullanswer_str[0:3]=='new':
        print("if fullanswer_str")
        fullanswer_str=fullanswer_str[3:]
        add_contents(request,fullanswer_str)
        
        #return_dic = cal_similarity(request, answer_str) #??
        #print(return_dic)

    return render(request,'main/index.html')

def add_contents(request,fullanswer_str):
    
    print("user test:",request.user.username)
    
    uc = ""
    
    return_dic = cal_similarity(request,answer_str)
    print(return_dic)
    
    if 'existed' in return_dic:
        category = return_dic.get('existed')
        uc = UserCategory.objects.get(inserted_category=category)
        topics = extract_topic(answer_str)
    elif 'new' in return_dic:
        topics = extract_topic(answer_str)
        topic_arr = topics.split("/")
        #content.topics = topics
        #category = get_category(topic_arr) <- 이 부분 확인 필요
        category = topic_arr[0]
        print("category is ", category)
        #user catergory id를 autofield로 만들면
        uc = UserCategory(inserted_category = category,user_id=request.user)
        uc.save()
        #uc = UserCategory.objects(inserted_category = category)
    else:
        print("no uc category")
    
    #content entity 생성 
    content=Content(answer=fullanswer_str,
                    user_id=request.user,
                    topics=topics,
                    inserted_category=uc)
                   
    
    content.save()

    return
            
    
    
def preprocessing_eng(data):
    tokenized = data['answer'].apply(lambda x: [word for word in x if len(word) > 2])
    detokenized = []
    for i in range(len(data)):
        t = ' '.join(tokenized[i])
        detokenized.append(t)
    context = detokenized
    #stop_words_list = stopwords.words('english')
    vectorizer = TfidfVectorizer(stop_words='english',max_features=10)
    X = vectorizer.fit_transform(context)
    
    return X, vectorizer 
    
'''
def preprocessing_kr(data):
    okt = Okt()
    tokenized = data['answer'].apply(lambda x: [word for word in okt.nouns(x)]) #명사로만 **
    detokenized = []
    for i in range(len(data)):
        t = ' '.join(tokenized[i])
        detokenized.append(t)
    context = detokenized
    vectorizer = TfidfVectorizer(max_features=10)
    X = vectorizer.fit_transform(context)
    
    return X, vectorizer
'''
    

#둘다 리스트로 보내서 돌려봐요,,
def get_category(top_features):
    selected_category=""
    userkeywords_set=UserCategory.objects.filter(user_id__name='hw')
    uk_list=[]
    for k in userkeywords_set:
        uk_list.append(k.name)

    print("???")
    print(top_features,uk_list)

    for item in top_features:
        if item in uk_list:
            selected_category=item
    
    return selected_category

