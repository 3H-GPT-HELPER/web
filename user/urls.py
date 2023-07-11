# user/urls.py

from django.urls import path
#from allauth.account.views import AccountProfileView
from . import views
urlpatterns = [
    # ...
    #path('accounts/profile/', AccountProfileView.as_view(), name='account_profile'),
    #path('profile/',views.google_profile),
    path('',views.index,name='kakao_index'),
    path('kakaoLogin/',views.kakaoLogin),
    path('kakaoLoginRedirect/',views.kakaoLoginRedirect),
    path('kakaoLogout/',views.kakaoLogout),
]
