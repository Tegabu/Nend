from email.mime import image
from urllib import request
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from socialspace.models import Profile, Post, likepost


@login_required(login_url='login')
def index(request):

    posts = Post.objects.all()
    return render(request, "landing/index.html", {'posts': posts})


@login_required(login_url='login')
def feed(request):
    return render(request, 'landing/feed.html')


@login_required(login_url='login')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')

    else:
        return redirect('/')
    return HttpResponse('<h1> hello! </h1>')


@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = likepost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = likepost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.num_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.num_likes -= 1
        post.save()
        return redirect('/')


@login_required(login_url='login')
def profile(request):
    # user_object = User.objects.get(username=pk)
    # user_profile = profile.objects.get(user=user_object)
    #  user_post = Post.objects.filter(user=pk)
    #  user_post_length = len(user_post)

    # context = {
    #    'user_object': user_object,
    #      'user_profile': user_profile,
    #     'user_post': user_post,
    #      'user_post_length': user_post_length,
    #     'posts': posts,
    #     }

    posts = Post.objects.all()
    return render(request, 'landing/profile.html')


@login_required(login_url='login')
def bookings(request):
    return render(request, 'landing/holiday.html')


@login_required(login_url='login')
def articles(request):
    return render(request, 'landing/articles.html')


@login_required(login_url='login')
def chat(request):
    return render(request, 'landing/chat.html')


@login_required(login_url='login')
def duka(request):
    return render(request, 'landing/duka.html')


@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    return render(request, 'landing/settings.html')


@login_required(login_url='login')
def podcast(request):
    return render(request, 'landing/podcast.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "invalid credentials")
            return redirect('login')
    else:
        return render(request, "landing/login.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'username taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.save()
                print("user created")

                # Profile object creation
                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'password not matching')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'landing/signup.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
