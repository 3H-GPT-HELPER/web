from django.contrib import admin
from django.urls import path,include
from . import views
from main.views import proxy
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    #path('login/', views.login, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='main/loginIndex.html'), name='loginIndex'),
    path('logout/',views.logout,name='logout'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('main/', views.main, name='main'),
    path('category/',views.category,name="category"),
    path('category/<int:pk>/',views.category_detail,name="detail_page"),
    path('proxy',views.proxy,name='proxy'),
    path('signout', views.signout, name='signout'),
    
]
 