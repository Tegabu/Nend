from email.mime import image
from urllib import request
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
import random

from socialspace.models import Profile, Post, likepost, product, Category, Host, FollowersCount, Listing
from .forms import NewListing


@login_required(login_url='login')
def index(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_objects)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(
        follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (
        x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(
        new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(user_id=ids)
        username_profile_list.append(profile_lists)

    suggestion_username_profile_list = list(chain(*username_profile_list))

    posts = Post.objects.all()
    return render(request, "landing/index.html", {'posts': posts, 'user_profile': user_profile, 'user_objects': user_objects, 'suggestion_username_profile_list': suggestion_username_profile_list[:10]})


@login_required(login_url='login')
def cart(request):
    context = {}
    return render(request, "landing/cart.html", context)


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
def new_listing(request):

    if request.method == 'POST':
        host_name = request.user.username
        category = Category.objects.all()
        img = request.FILES.get('img')
        description = request.POST.get('description', False)
        charge = request.POST.get('charge', False)
        location = request.POST.get('location', False)
        name = request.POST.get('name', False)

        new_Listing = Listing.objects.create(category=category,
                                             img=img, description=description, charge=charge, location=location, name=name)
        new_listing.save()

        return redirect(request, 'landing/listing.html', {'category': category})

    else:
        return redirect(request, 'landing/settings.html')


@ login_required(login_url='login')
def sell(request):
    context = {}
    return render(request, "landing/cart.html", context)


@ login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = likepost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = likepost.objects.create(
            post_id=post_id, username=username)
        new_like.save()
        post.num_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.num_likes -= 1
        post.save()
        return redirect('/')


@ login_required(login_url='login')
def user(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)

    posts = Post.objects.all()
    hosts = Host.objects.all()

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {'posts': posts, 'hosts': hosts,
               'user_object': user_object, 'user_profile': user_profile, 'user_post': user_post,
               'user_post_length': user_post_length, 'button_text': button_text, 'user_followers': user_followers, 'user_following': user_following}

    return render(request, 'landing/profile.html', context)


@ login_required(login_url='login')
def base(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)

    context = {'user_profile': user_profile, 'user_post': user_post,
               'user_post_length': user_post_length}
    return render(request, 'landing/base.html', context, )


@ login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delet_follower = FollowersCount.objects.get(
                follower=follower, user=user)
            delet_follower.delete()
            return redirect('/user/'+user)
        else:
            new_follower = FollowersCount.objects.create(
                follower=follower, user=user)
            new_follower.save()
            return redirect('/user/'+user)
    else:
        return redirect('/')


@ login_required(login_url='login')
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
    profile = Profile.objects.all()
    hosts = Host.objects.all()
    users = User.objects.all()
    categories = Category.objects.all()
    context = {'categories': categories, 'posts': posts,
               'hosts': hosts, 'profile': profile, 'user': users}

    return render(request, 'landing/profile.html', context)


@ login_required(login_url='login')
def bookings(request):
    listings = Listing.objects.filter(is_available=True)[0:10]
    categories = Category.objects.all()

    context = {'categories': categories, "listings": listings}
    return render(request, 'landing/holiday.html', context)


@ login_required(login_url='login')
def detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    related_listings = Listing.objects.filter(
        category=listing.category, is_available=True).exclude(pk=pk)[0:4]

    context = {'listing': listing, 'related_listings': related_listings}

    return render(request, 'landing/listing.html', context)


@ login_required(login_url='login')
def new(request):
    form = NewListing()

    return render(request, 'landing/settings.html', {'form': form})


@ login_required(login_url='login')
def addlisting(request):
    if request.method == 'POST':
        form = NewListing(request.POST, request.FILES)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.host_name = request.user
            listing.save()

            return redirect('social:new_listing', pk=listing.id)

    else:
        form = NewListing()

        return render(request, 'landing/addlisting.html', {'form': form})


@ login_required(login_url='login')
def chat(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)

    return render(request, 'landing/chat.html', {'user_profile': user_profile,  'user_objects': user_objects})


@ login_required(login_url='login')
def duka(request):
    context = {}
    return render(request, 'landing/duka.html', context)


@ login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            phone = request.POST['phone']
            email = request.POST['email']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.phone = phone
            user_profile.email = email
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            phone = request.POST['phone']
            email = request.POST['email']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.phone = phone
            user_profile.email = email
            user_profile.save()
        return redirect('social:profile')
    return render(request, 'landing/settings.html', {'user_profile': user_profile, 'categories': categories})


@ login_required(login_url='login')
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
                return redirect('profile')
        else:
            messages.info(request, 'password not matching')
            return redirect('register')
        return redirect('/')

    else:
        return render(request, 'landing/signup.html')


@ login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
