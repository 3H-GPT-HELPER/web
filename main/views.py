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
from user.models import UserCategory

#pip install nltk, scikit-learn, pandas, konlpy 필요
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 

import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

from konlpy.tag import Okt

import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def index(request):
    users = User.objects.all()

    for user in users:
        print(user.email)

    return render(request,'main/index.html')

def signup(request):

    if request.method == "POST":
        email = request.POST['Email']
        name = request.POST['Name']
        password = request.POST['Password']

        myuser = User.objects.create_user(email, name, password)
        # myuser.name = name
        
        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('login')

    return render(request,"main/signup.html")

def login(request):

    if request.method=="POST":
            email = request.POST['Email']
            password = request.POST['Password']

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                # name = user.name
                return render(request, 'main/index.html') # , {'name': Name}

            else:
                messages.error(request, "Bad Credentials!")
                return redirect(index)

    return render(request, 'main/login.html')

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
    #preprocessing(userContents)
    
    return render(request, 'main/main.html',context=context)

def category(request):
    print("user",request.user)
    userCategories=UserCategory.objects.filter(user_id__user_id=request.user.user_id)
    context={'userCategories':userCategories}
   
    return render(request,"main/category.html",context=context)

def category_detail(request,category_id):

    #category_id는 자동생성 및 전달되는 pk
    uc=UserCategory.objects.get(userCategory_id=category_id)
    
    uc_name=uc.inserted_category
    category_id=uc.userCategory_id
    userContents=Content.objects.filter(inserted_category=uc_name)
    context={'contents':userContents,'category_id':category_id}

    return render(request,'main/detail.html',context=context)


@csrf_exempt
def proxy(request):
    if request.method == 'POST':    
        try:
            data=json.loads(request.body.decode('utf-8'))
            answer=data['pTagContents']
            full_answer=data['complexContents']
            
            answer_str = ''.join(answer) #text만 있는 답변
            fullanswer_str = ''.join(full_answer) #코드까지 합쳐진 답변
            
            print(answer_str)
            print(fullanswer_str)

            #content entity 생성 
            content=Content(answer=fullanswer_str)

            topics = extract_topic(answer_str)

            topic_arr = topics.split("/")
            content.topics = topics

            category=get_category(topic_arr)
            print(category)

            content.selected_category=category

            content.save()
            

        except json.JSONDecodeError:
            return HttpResponseBadRequest('invalid json data')
        
        
        print("main으로 보내버려~")
       

    return JsonResponse({'error': 'Invalid request method'})

def extract_topic(answer):    
    data = pd.DataFrame({'answer':[answer]})
    data['answer'] = data.apply(lambda row: nltk.word_tokenize(row['answer']),axis=1)
    
    #영어/한국어 구분 **
    if data['answer'].encode().isalpha():
        X, vectorizer = preprocessing_eng(data)
    else:
        X, vectorizer = preprocessing_kr(data)
    
    lda_model = LatentDirichletAllocation(n_components=1, learning_method='online', random_state=777, max_iter=3)
    lda_top = lda_model.fit_transform(X)
    
    topic = get_topics(lda_model.components_,vectorizer.get_feature_names_out())
    topics= '/'.join(topic)
    
    return topics
    
    
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
def get_category(request,top_features):
    selected_category=""
    #userkeywords_set=UserCategory.objects.filter(user_id__name='hw')
    userkeywords_set=UserCategory.objects.filter(user_id__user_id=request.user.user_id)
    uk_list=[]
    for k in userkeywords_set:
        uk_list.append(k.inserted_category)

    print("???")
    print(top_features,uk_list)

    for item in top_features:
        if item in uk_list:
            selected_category=item
    
    return selected_category

