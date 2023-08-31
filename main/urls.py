from django.urls import path,include
from . import views
from main.views import proxy

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('main/', views.main, name='main'),
    path('category/',views.category,name="category"),
    path('category/<int:category_id>/',views.category_detail,name="detail_page"),
    path('proxy',views.proxy,name='proxy'),

    
]
