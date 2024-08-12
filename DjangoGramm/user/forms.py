from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', min_length=3, max_length=30)
	email = forms.EmailField()
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
