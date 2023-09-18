from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Users


class SignupForm(UserCreationForm):
    class Meta():
        model = Users
        fields = ['email', 'username','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username']
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'example@example.com'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': '8자 이상 15자 이하의 영문,숫자만 가능'})
        self.fields['password2'].widget.attrs.update()
        
        