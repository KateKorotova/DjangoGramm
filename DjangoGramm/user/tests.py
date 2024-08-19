from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser
from .forms import UserRegisterForm, UserProfileForm


class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('edit_profile')
        self.confirm_email_url_name = 'confirm_email'
        self.email_confirmation_sent_url = reverse('email_confirmation_sent')

        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword123', is_active=True,
            first_name='test', last_name='test'
        )

    def test_register_view_post(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'test',
            'last_name': 'test',
        })
        self.user.refresh_from_db()
        new_user = CustomUser.objects.get(username='newuser')
        self.assertFalse(new_user.is_active)  # User should be inactive until email confirmation

    def test_confirm_email_view(self):
        user = CustomUser.objects.create_user(
            username='newuser', email='newuser@example.com', password='newpassword123', is_active=False
        )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = reverse(self.confirm_email_url_name, kwargs={'uidb64': uid, 'token': token})

        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.is_active)  # User should be active after email confirmation

    def test_email_confirmation_sent_view(self):
        response = self.client.get(self.email_confirmation_sent_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_confirmation_sent.html')

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword123')
        user = CustomUser.objects.get(username='testuser')
        response = self.client.post(self.profile_url, {
            'first_name': 'updatedtest',
            'last_name': user.last_name,
            'bio': user.bio,
            'avatar': user.avatar,
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'updatedtest')

    def test_login_view_post(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('feed'))

    def test_login_view_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)

    def test_edit_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIsInstance(response.context['form'], UserProfileForm)
