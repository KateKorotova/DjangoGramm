from django.urls import path
from .views import post_feed, user_profile, add_post, post_detail, toggle_like

urlpatterns = [
    path('', post_feed, name='feed'),
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('feed/', post_feed, name='feed'),
    path('user_profile/<str:username>/', user_profile, name='user_profile'),
    path('add-post/', add_post, name='add_post'),
    path('toggle-like/', toggle_like, name='toggle_like')
]
