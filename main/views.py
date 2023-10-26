from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest,HttpResponseRedirect
from django.middleware.csrf import get_token


from httpx import Auth
from django.contrib import auth
from .forms import SignupForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.http.request import HttpRequest
from .models import Content
from user.models import UserCategory
#pip install nltk, scikit-learn, pandas, konlpy 필요
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 

import pandas as pd
from collections import deque

nltk.download('punkt')
nltk.download('stopwords')

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import numpy as np
import sys
#sys.path.append('/Users/hgy/Desktop/hgy/EWHA/2023_1(4)/Final_project/3H/main')
from .cal_similarity import cal_similarity
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .extract_topic import *

fullanswer_str=""
answer_str=""
answer_list=[]
answer_list=deque(answer_list)

question_list=[]
question_list=deque(question_list)

authenticated=False
username=""

def signup(request: HttpRequest, *args, **kwargs):
    if request.method=='POST':
        username = request.POST.get('username')
        email=request.POST.get('email')
        password = request.POST.get('password2')
        user=User.objects.create_user(email=email, username=username, password=password)
        #print(user.username,email,user.password)
        user.save()
        return redirect('/')
        
    else:
        form=SignupForm()
        return render(request,"main/signup.html",{"form":form})

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        userEmail=request.POST.get('userEmail')
        userpassword=request.POST.get('password')

        #huda 해결해야하는 부분
        user = auth.authenticate(
            request,username=username,password=userpassword)
        
        if user is not None:
            auth.login(request,user)
            print("login success")
            return render(request,"main/login_success.html")

        else:
            print("login failed")
            return render(request, 'main/login.html')

    else:
        return render(request, 'main/login.html')

from django.contrib.auth import logout as auth_logout
def logout(request):
    auth_logout(request)
    return redirect('/')    

def signout (request):
    logout(request)
    messages.success(request, "Logged out succesfully!")
    return redirect(index)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def main(request):
    print("this is main page")
    
    userContents=Content.objects.filter(userName="hw")
    context={'contents':userContents}
    
    return render(request, 'main/main.html',context=context)

def category(request):

    #chat gpt사이트에서 받아온 답변들 추가하는 코드
    global fullanswer_str
    global answer_str

    while answer_list:
        print(question_list)
        
        fullanswer_str=answer_list.popleft()
        question_str=question_list.popleft()

        print("\n????",question_str)
        if fullanswer_str[0:3]=='new':
            #print("if fullanswer_str")
            fullanswer_str=fullanswer_str[3:]
            add_contents(request,fullanswer_str,question_str)

    ## category 새로 생성시 코드
    if request.method == 'POST':
        new_category = request.POST.get('new_category')
        if new_category:
            print("category add !",request.user.username)
            new=UserCategory.objects.create(inserted_category=new_category, user_id=request.user)
            new.save()
            
            return redirect('category') 
        else:
            return JsonResponse({'message': 'Category name is required'}, status=400)
    
    ##
    userCategories=UserCategory.objects.filter(user_id__username=request.user.username)

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
    userContents=Content.objects.filter(inserted_category__inserted_category=uc_name,user_id__username=request.user.username)
    context={'contents':userContents,'category_id':category_id}

    return render(request,'main/detail.html',context=context)

from django.http import JsonResponse
@csrf_exempt
def proxy(request):
    if request.method=='GET':
        print("authenticated test2",authenticated)
        if authenticated:
            print("chrome login check:",username)
            return JsonResponse({'authenticated': 'True', 'username': username})
        else:
            print("not login,,,,")
            return JsonResponse({'authenticated': 'False'})
        
    if request.method == 'POST':    
        try:
            data=json.loads(request.body.decode('utf-8'))
            
            #chat gpt 사이트로 부터 질문, 답변 jsonresponse 받기
            answer=data['pTagContents']
            full_answer=data['complexContents']
            question_text=data['questionText']
            
            global fullanswer_str
            global answer_str
            
            answer_str = ''.join(answer) #text만 있는 답변
            fullanswer_str='new'
            fullanswer_str += ''.join(full_answer) #코드까지 합쳐진 답변

            answer_list.append(fullanswer_str)
            question_list.append(question_text)
            
        except json.JSONDecodeError:
            return HttpResponseBadRequest('invalid json data')
        
    return JsonResponse({'error': 'Invalid request method'})

def index(request):
    if request.user.is_authenticated:
        global authenticated
        authenticated=True          
        global username
        username=request.user.username
            
    return render(request,'main/index.html')

def add_contents(request,answer_str,question_str):
    
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
        #category = get_category(topic_arr) <- 이 부분 확인 필요
        category = topic_arr[0]
        print("category is ", category)
        
        try:
            if UserCategory.objects.get(inserted_category=category,user_id=request.user) != None:
                uc = UserCategory.objects.get(inserted_category = category,user_id=request.user)
                print("try if")
            else:
                uc = UserCategory(inserted_category = category,user_id=request.user)
                uc.save()
                print("try else")
        except:
            uc = UserCategory(inserted_category = category,user_id=request.user)
            uc.save()
            print("except")
    else:
        print("no uc category")

    print("entity생성 전 category 확인",category)
    
    #content entity 생성 
    content=Content(answer=fullanswer_str,
                    user_id=request.user,
                    question=question_str,
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

