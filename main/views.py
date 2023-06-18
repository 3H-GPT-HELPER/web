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
            answer=answer[0]
            print("!!!!!!!!!!!!!!!!!!!!!!")
            print(answer)
            
            #entity 생성 
            content=Content(answer=answer)
            content.save()

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