import os
import django
from django.core.files import File

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoGramm.settings')
django.setup()

from user.models import CustomUser
from post.models import Post, Image, Tag, Like

def create_users():
    user1 = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='password123')
    user2 = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='password123')
    print(f"Created users: {user1.username}, {user2.username}")
    return user1, user2

def create_images():
    with (open('media/images/F_F20CAPETOWN_3B.jpg', 'rb') as img1,
          open('media/images/on-the-shore-borrowdale-and-derwent-water-1518851.jpg', 'rb') as img2):
        image1 = Image.objects.create(image=File(img1), alt_text='Image 1')
        image2 = Image.objects.create(image=File(img2), alt_text='Image 2')
    print(f"Created images: {image1.alt_text}, {image2.alt_text}")
    return image1, image2

def create_tags():
    tag1 = Tag.objects.create(name='tag1')
    tag2 = Tag.objects.create(name='tag2')
    print(f"Created tags: {tag1.name}, {tag2.name}")
    return tag1, tag2

def create_posts(user1, user2, image1, image2, tag1, tag2):
    post1 = Post.objects.create(user=user1)
    post2 = Post.objects.create(user=user2)

    post1.images.add(image1)
    post1.tags.add(tag1)

    post2.images.add(image2)
    post2.tags.add(tag2)

    print(f"Created posts for users: {user1.username}, {user2.username}")
    return post1, post2

def create_likes(post1, post2, user1, user2):
    Like.objects.create(user=user1, post=post2)
    Like.objects.create(user=user2, post=post1)
    print(f"Created likes for posts: {post1.id}, {post2.id}")

def run():
    user1, user2 = create_users()
    image1, image2 = create_images()
    tag1, tag2 = create_tags()
    post1, post2 = create_posts(user1, user2, image1, image2, tag1, tag2)
    create_likes(post1, post2, user1, user2)

if __name__ == '__main__':
    CustomUser.objects.filter(username__in=['user1', 'user2']).delete()
    run()
