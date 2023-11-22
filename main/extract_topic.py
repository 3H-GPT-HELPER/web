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
from user.models import UserCategory
#pip install nltk, scikit-learn, pandas, konlpy 필요
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
from nltk.stem import PorterStemmer

nltk.download('tagsets')
nltk.download('averaged_perceptron_tagger')

from nltk.tag import pos_tag

import pandas as pd


import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def extract_topic(answer):    
    data = pd.DataFrame({'answer':[answer]})
    data['answer'] = data.apply(lambda row: nltk.word_tokenize(row['answer']),axis=1)
    
    #영어/한국어 구분 **
    #if data['answer'].encode().isalpha():
    X, vectorizer = preprocessing_eng(data)
    #else:
    #    X, vectorizer = preprocessing_kr(data)
    
    lda_model = LatentDirichletAllocation(n_components=1, learning_method='online', random_state=777, max_iter=3)
    lda_top = lda_model.fit_transform(X)
    
    topic = get_topics(lda_model.components_,vectorizer.get_feature_names_out())
    topics= '/'.join(topic)
    
    return topics

def get_topics(components, feature_names, n=3):
    topic = []
    
    for idx, topic in enumerate(components):
       # top_features = [(feature_names[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]]
       top_features = [feature_names[i] for i in topic.argsort()[:-n - 1:-1]]

    print(top_features)
        
    return top_features

def preprocessing_eng(data):
    stop_words_list = stopwords.words('english')
    #tokenized = data['answer'].apply(lambda x: [word for word in x if len(word)>2])
    
    tokenized = data['answer'].apply(lambda x: [word for word in x if (len(word) > 2 
                                                                       and word not in stop_words_list 
                                                                       and pos_tag([word])[0][1]=='NN'
                                                                       or pos_tag([word])[0][1]=='NNP'
                                                                       and pos_tag([word])[0][1]!='VB'
                                                                       )])
    
    lmtzr = WordNetLemmatizer()
    tokenized = data['answer'].apply(lambda x: [lmtzr.lemmatize(word) for word in x])
    #tokenized = data['answer'].apply(lambda x: [lmtzr.lemmatize(word,'v') for word in x])
    
    #stemmer = PorterStemmer()
    #tokenized = data['answer'].apply(lambda x: [stemmer.stem(word) for word in x])
    
    detokenized = []
    for i in range(len(data)):
        t = ' '.join(tokenized[i])
        detokenized.append(t)
    context = detokenized
    print("detokenized--------",context)
    vectorizer = TfidfVectorizer(stop_words='english',max_features=10)
    X = vectorizer.fit_transform(context)
    
    return X, vectorizer 