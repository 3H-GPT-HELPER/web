from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
import json
from django.contrib import auth

from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User


#kakao login(나중에 settings.py나 secrets.json으로 옮기기)
restApiKey='ab143070c987ae072f64e7796aa6622a'
#redirectUrl='http://127.0.0.1:8000/accounts/kakao/login/callback'
redirectUrl='http://127.0.0.1:8000/user/kakaoLoginRedirect'
client_secret='oEMteera7gGjo8No8Ix7XqM5CRnjvqqc'
admin_key='2f9ce4cfd61a8a8afb7654b11bd7e243'

    
def index(request):
    context={'check':False}

    if request.session.get('access_token'):
        context['check']=True

    print(context['check'])
    return render(request,'user/kakao_index.html',context)

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
@csrf_exempt
def login(request):
    if request.method == 'POST':
        #username=request.POST.get('username')
        userEmail=request.POST.get('userEmail')
        userpassword=request.POST.get('password')

        print(userEmail,userpassword)

        #huda 해결해야하는 부분
        user = auth.authenticate(
            request, password=userpassword,email=userEmail)
        
        if user is not None:
            auth.login(request,user)
            print("login success")
    
            return render(request,"user/login_success.html")

        else:
            print("try again")
            return redirect(request, 'login.html')

    else:
        #return render(request, 'user/login.html', context)
        return render(request, 'login.html')


def loginSuccess(request):
    return render(request,"login_success.html")

def logout(request):
    return render(request,'user/logout_success.html')

def kakaoLogin(request):
    url=f'https://kauth.kakao.com/oauth/authorize?client_id={restApiKey}&redirect_uri={redirectUrl}&response_type=code'
    
    return redirect(url)

def kakaoLoginRedirect(request):
    code=request.GET['code']
    #url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={restApiKey}&redirect_uri={redirectUrl}&code={code}'
    url="https://kauth.kakao.com/oauth/token"
    res={
        'grant_type':'authorization_code',
        'client_id':restApiKey,
        'redirect_uri':redirectUrl,
        'client_secret':client_secret,
        'code':code
    }
    
    headers={
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    response=requests.post(url,data=res,headers=headers)

    tokenJson=response.json()

    
    #get userInfo
    userUrl = "https://kapi.kakao.com/v2/user/me"
    auth='Bearer '+tokenJson['access_token']
    header={
        'Authorization':auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    res=requests.get(userUrl,headers=header)
    try:
        info=res.json()
    except:
        info=None
    #print(info)
    kakao_id=str(info.get("id"))

    # print(info,kakao_id)

    try:
        test=User.objects.get(user_id=kakao_id)
    except User.DoesNotExist:
        test=None

    print(test)
    if test is None:
        nickname="default"
        email='default'
        user_info=info.get("kakao_account")
        # agree_on_nickname=user_info.get("profile_nickname_needs_agreement")
        # if not agree_on_nickname:
        #     profile=user_info.get("profile")
        #     nickname=profile.get('nickname')

        agree_on_nickname=user_info.get('profile_needs_agreement')
        print(agree_on_nickname)
        if not agree_on_nickname:
            profile=user_info.get("profile")
            nickname=profile['nickname']
        
        agree_on_email=user_info.get('eamil_needs_agreement')

        print(agree_on_email)

        if not agree_on_email:
            email=user_info.get('email')
        
        # print(nickname,email,kakao_id)

        print("!!!!")
        user=Users(
            name=nickname,
            email_address=email,
            user_id=kakao_id,
            password="",
        )
        print("?????")
        print(user)
        #user.backend = f"{ModelBackend.__module__}.{ModelBackend.__name__}"
        user.save()

        # Authenticate the user
        authenticated_user = authenticate(request, username=user.name, password="")
        if authenticated_user is not None:
            login(request, authenticated_user)  # 사용자를 로그인 상태로 만듭니다.
            return render(request,'user/login_success.html')
        
        else:
            return HttpResponse("login failed, try again.")

    else:
        print(test)
        redirect("http://127.0.0.1:8000/") 
    
    


def kakaoLogout(request):
    print(request.user)
    kakao_id=request.user.user_id
    token=request.session['access_token']
    url='https://kapi.kakao.com/v1/user/logout'
    header={
        'Authorization':f'bearer {token}'
    }

    res=requests.post(url,headers=header)
    result=res.json()
    # target_id=request.user.kakao_id
    # target_id=int(target_id)
    # auth='KakaoAK'+admin_key
    # headers={
    #     'Authorization':auth,
    #     "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    # }

    # data={
    #     'target_id_type':'user_id',
    #     'target_id':target_id
    # }

    # res=requests.post(
    #     url,headers=headers,data=data
    # ).json()

    response=res.get("id")

    if kakao_id!=response:
        return render(request,'user/logoutError.html')
    
    else:
        return render(request,'user/loginout_success.html')
    # if result.get('id'):
    #     del request.session['access_token']
    #     return render(request,'user/loginout_success.html')
    # else:
    #     return render(request,'user/logoutError.html')

def kakaoLogout_all(reqeust):
    redirect_url='http://127.0.0.1:8000/user/kakaoLogout'
    state="none"
    kakao_service_logout_url='https://kauth.kakao.com/oauth/logout'

    return redirect(
        f"{kakao_service_logout_url}?client_id={restApiKey}&logout_redirect_uri={redirect_url}"
    )
    


