from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('email-confirmation-sent/', views.email_confirmation_sent, name='email_confirmation_sent'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
]

