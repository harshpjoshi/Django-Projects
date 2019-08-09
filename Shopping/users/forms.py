from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfileModel

class UserResgister(UserCreationForm):
    '''
        this is user register form can used in view file for creating form
    '''
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class UserUpdate(forms.ModelForm):
    '''
        this is user update form can used in view file for updating profile
    '''
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username']

class ProfileUpdate(forms.ModelForm):
    '''
        this is user profile image update form can used in view file for updating profile
    '''
    class Meta:
        model = ProfileModel
        fields = ['image']
