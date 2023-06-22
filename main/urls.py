from django.urls import path
from . import views
from main.views import proxy

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('main/', views.main, name='main'),
    path('category/',views.category,name="category"),
    path('category/<int:category_id>/',views.category_detail,name="detail_page"),
    path('proxy',views.proxy,name='proxy'),
    
]
