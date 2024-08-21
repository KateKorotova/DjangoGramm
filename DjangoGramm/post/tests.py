from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages

from .models import Post, Image, Tag

CustomUser = get_user_model()


class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.other_user = CustomUser.objects.create_user(username='otheruser', email='other@example.com', password='password123')
        self.post = Post.objects.create(user=self.user)
        self.image = Image.objects.create(image='test.jpg', alt_text='test image')
        self.tag = Tag.objects.create(name='testtag')
        self.post.images.add(self.image)
        self.post.tags.add(self.tag)

    def test_user_profile_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        self.assertContains(response, self.user.username)

    def test_user_profile_view_unauthenticated(self):
        response = self.client.get(reverse('user_profile', args=[self.user.username]))
        self.assertRedirects(response, f'/login/?next=/user_profile/{self.user.username}/')

    def test_post_feed_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_feed.html')

    def test_post_feed_view_unauthenticated(self):
        response = self.client.get(reverse('feed'))
        self.assertRedirects(response, '/login/?next=/feed/')

    def test_toggle_like_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('toggle_like'), {'post_id': self.post.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'liked': True,
            'like_count': 1
        })
        # Test unlike
        response = self.client.post(reverse('toggle_like'), {'post_id': self.post.id})
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'liked': False,
            'like_count': 0
        })

    def test_add_post_view_get_request(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('add_post'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn('html', response.json())

    def test_add_post_view_post_request(self):
        self.client.login(username='testuser', password='password123')
        with open('test_image.jpg', 'wb') as f:
            f.write(b'\x00\x00\x00\x00')
        with open('test_image.jpg', 'rb') as image:
            response = self.client.post(reverse('add_post'), {'images': [image], 'tags': 'tag1,tag2'}, follow=True)
        self.assertRedirects(response, reverse('user_profile', args=[self.user.username]))
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Tag.objects.count(), 3)

    def test_add_post_view_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        invalid_file = SimpleUploadedFile("test.pdf", b"\x00\x00\x00\x00", content_type="application/pdf")
        response = self.client.post(reverse('add_post'), {
            'images': invalid_file,
            'tags': 'test'
        })
        response = self.client.get(reverse('user_profile', args=[self.user.username]))
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[0].level_tag, 'error')
