# user/urls.py

from django.urls import path
#from allauth.account.views import AccountProfileView

from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # ...
    #path('accounts/profile/', AccountProfileView.as_view(), name='account_profile'),
    #path('profile/',views.google_profile),
    path('',views.index,name='kakao_index'),
    #path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='user_login'),
    path('login/',views.login,name='user_login'),
    path('login_success/',views.loginSuccess,name="login_success"),
    path('logout/',views.logout,name='user_logout'),
    path('kakaoLogin/',views.kakaoLogin),
    path('kakaoLoginRedirect/',views.kakaoLoginRedirect),
    path('kakaoLogout/',views.kakaoLogout),
]
