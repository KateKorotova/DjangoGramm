from django.urls import path
from django.contrib.auth import views as auth

from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='main_feed.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name='email_confirmation_sent'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
