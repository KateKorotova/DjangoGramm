from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'bio', 'avatar']
		widgets = {
			'avatar': forms.ClearableFileInput(attrs={'multiple': False}),
			'bio': forms.Textarea(attrs={'rows': 3}),
		}

	def clean_images(self):
		images = self.cleaned_data.get('images')
		if images:
			if not images.content_type.startswith('image/'):
				raise ValidationError('Only image files are allowed.')
		return images


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', min_length=3, max_length=30)
	email = forms.EmailField()
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

	def clean_images(self):
		images = self.cleaned_data.get('images')
		if images:
			if not images.content_type.startswith('image/'):
				raise ValidationError('Only image files are allowed.')
		return images

