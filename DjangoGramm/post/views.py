from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import OuterRef, Exists

from user.models import CustomUser

from .forms import ImageForm, TagForm
from .models import Post, Image, Tag, Like


@login_required(login_url="/login/")
def user_profile(request, username):
    user = CustomUser.objects.get(username=username)
    posts = Post.objects.filter(user=user).prefetch_related('images', 'tags').annotate(
        liked=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
    ).order_by('-created_dt')
    return render(request, 'user_profile.html', {'user': user, 'posts': posts})


@login_required(login_url="/login/")
def post_feed(request):
    posts = Post.objects.all().prefetch_related('images', 'tags').annotate(
        liked=Exists(Like.objects.filter(user=request.user, post=OuterRef('pk')))
    ).order_by('-created_dt')
    return render(request, 'main_feed.html', {'posts': posts})


@login_required
def toggle_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)

        liked = False
        if post.like_set.filter(user=request.user).exists():
            post.like_set.filter(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True

        return JsonResponse({'liked': liked, 'like_count': post.like_set.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url="/login/")
def add_post(request):
    if request.method == 'POST':
        image_form = ImageForm(request.FILES)
        tag_form = TagForm(request.POST)

        if image_form.is_valid() and tag_form.is_valid():
            post = Post.objects.create(user=request.user)

            # Handle images
            images = request.FILES.getlist('images')
            for image in images:
                img = Image.objects.create(image=image, alt_text=image.name)
                post.images.add(img)

            # Handle tags
            tags = tag_form.cleaned_data['tags'].split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                post.tags.add(tag)

            post.save()
            return redirect('user_profile', request.user.username)
        else:
            error_message = 'Errors: ' + '; '.join(image_form.errors['images'].as_text().splitlines())
            messages.error(request, error_message)
    else:
        image_form = ImageForm()
        tag_form = TagForm()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('partials/add_post_modal_body.html', {
            'images': image_form,
            'tags': tag_form
        }, request=request)
        return JsonResponse({'html': html})

    return redirect('user_profile', request.user.username)
