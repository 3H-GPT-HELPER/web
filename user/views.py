from django.shortcuts import render

# views.py

from allauth.socialaccount.models import SocialAccount

def google_profile(request):
    try:
        # 현재 로그인된 사용자 가져오기
        user = request.user
        
        # SocialAccount 모델을 통해 Google Social Account 가져오기
        social_account = SocialAccount.objects.get(user=user, provider='google')
        
        # Google에서 제공하는 사용자 정보 가져오기
        extra_data = social_account.extra_data
        google_email = extra_data.get('email')
        google_name = extra_data.get('name')
        
        # 추가 작업 수행
        # ...
        
    except SocialAccount.DoesNotExist:
        # Social Account가 없는 경우 처리
        pass
    
    context={
        'google_email':google_email,
        'google_name':google_name,
    }

    return render(request,'user/profile.html',context)
    
