from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .forms import UserRegisterForm, UserProfileForm
from .models import CustomUser
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

load_dotenv()
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False  # Deactivate account until it is confirmed
			user.save()

			token = default_token_generator.make_token(user)
			uid = urlsafe_base64_encode(force_bytes(user.pk))
			confirmation_link = request.build_absolute_uri(
				reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
			)

			subject = 'Confirm your email'
			message = render_to_string('email_confirmation.html', {
				'user': user,
				'confirmation_link': confirmation_link,
			})

			email = EmailMultiAlternatives(subject, '',  EMAIL_HOST_USER, [user.email])
			email.attach_alternative(message, "text/html")
			email.send()

			# messages.success(request, 'Please confirm your email to complete registration.')
			return redirect('email_confirmation_sent')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form, 'title': 'Register here'})


def confirm_email(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = CustomUser.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Your email has been confirmed. You can now log in.')
		login(request, user)
		return redirect('edit_profile')
	else:
		messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
		return redirect('feed')


def email_confirmation_sent(request):
	return render(request, 'email_confirmation_sent.html')


@login_required(login_url="/login/")
def edit_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated.')
			return redirect('user_profile', username=request.user.username)
		else:
			messages.error(request, form.errors.as_text().splitlines())
	else:
		form = UserProfileForm(instance=request.user)
	return render(request, 'edit_profile.html', {'form': form, 'user': request.user})


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('feed')
	else:
		form = AuthenticationForm()

	return render(request, 'login.html', {'form': form, 'title': 'Log in'})
