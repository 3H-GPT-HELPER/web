# user/urls.py

from django.urls import path
#from allauth.account.views import AccountProfileView
from . import views
urlpatterns = [
    # ...
    #path('accounts/profile/', AccountProfileView.as_view(), name='account_profile'),
    path('profile/',views.google_profile),
]
