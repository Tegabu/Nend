from email.mime import image
from urllib import request
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from itertools import chain
from django.db.models import Q
import random

from socialspace.models import Profile, Post, likepost, product, Category, Host, FollowersCount, Listing,  profile_pic
from .forms import NewListing, EditListing


def index(request):
    try:
        user_objects = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_objects)
    except:
        user_objects = 'anonymous'
        user_profile = 'anonymous'

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
        try:
            user_list = User.objects.get(username=user.user)
        except:
            user_list = None
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

    posts = [x for x in list(Post.objects.all())]
    random.shuffle(posts)
    return render(request, "landing/index.html", {'posts': posts,  'user_profile': user_profile, 'user_objects': user_objects, 'suggestion_username_profile_list': suggestion_username_profile_list[:10]})

# search bar


@login_required(login_url='login')
def search_bar(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    category = Category.objects.all
    listings = Listing.objects.filter(
        Q(is_available=True) | Q(description__icontains=query))

    if category_id:
        listings = listings.filter(category_id=category_id)

    if query:
        listings = listings.filter(name__icontains=query)

    return render(request, 'landing/search.html', {'user_objects': user_objects, 'user_profile': user_profile, 'listings': listings, 'query': query, 'category': category, 'category_id': int(category_id)})


def find(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(user_id=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    return render(request, 'landing/find.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


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
        return JsonResponse({'likedStatus': 1, 'likes': post.num_likes})
    else:
        like_filter.delete()
        post.num_likes -= 1
        post.save()
        return JsonResponse({'likedStatus': 0, 'likes': post.num_likes})


@ login_required(login_url='login')
def user(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)
    listings = Listing.objects.filter(host_name=user_object)

    listing_len = len(listings)

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

    context = {'posts': posts, 'hosts': hosts, 'listing_len': listing_len, 'listings': listings,
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


# Chat functions


# Dashboard views

@ login_required(login_url='login')
def dashboard(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    listings = Listing.objects.filter(host_name=request.user)
    posts = Post.objects.all()

    return render(request, 'landing/dashboard.html', {'posts': posts, 'listings': listings, 'user_profile': user_profile,  'user_objects': user_objects})


@ login_required(login_url='login')
def delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, host_name=request.user)
    listing.delete()

    return redirect('social:dashboard')


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


def bookings(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    listings = [x for x in list(
        Listing.objects.filter(is_available=True)[0:12])]
    categories = Category.objects.all()

    random.shuffle(listings)

    context = {'categories': categories, "listings": listings,
               'user_profile': user_profile,  'user_objects': user_objects}
    return render(request, 'landing/holiday.html', context)


@ login_required(login_url='login')
def detail(request, pk):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    listing = get_object_or_404(Listing, pk=pk)
    related_listings = Listing.objects.filter(
        category=listing.category, is_available=True).exclude(pk=pk)[0:6]

    context = {'listing': listing, 'related_listings': related_listings,
               'user_profile': user_profile,  'user_objects': user_objects}

    return render(request, 'landing/listing.html', context)


# New listings Add
@ login_required(login_url='login')
def new(request):
    form = NewListing()

    return render(request, 'landing/settings.html', {'form': form})


@ login_required(login_url='login')
def addlisting(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = NewListing(request.POST, request.FILES)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.host_name = request.user
            listing.save()

            return redirect('social:detail', pk=listing.id)

    else:
        form = NewListing()

    return render(request, 'landing/addlisting.html', {'form': form, 'user_profile': user_profile,  'user_objects': user_objects})


@ login_required(login_url='login')
def editlisting(request, pk):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    listing = get_object_or_404(Listing, pk=pk, host_name=request.user)

    if request.method == 'POST':
        form = EditListing(request.POST, request.FILES, instance=listing)

        if form.is_valid():
            form.save()

            return redirect('social:detail', pk=listing.id)

    else:
        form = EditListing(instance=listing)

    return render(request, 'landing/edit_listing.html', {'form': form, 'user_profile': user_profile,  'user_objects': user_objects})


@ login_required(login_url='login')
def chat(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)

    return render(request, 'landing/chat.html', {'user_profile': user_profile,  'user_objects': user_objects})


@ login_required(login_url='login')
def duka(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)
    listings = Listing.objects.filter(host_name=request.user)
    post = Post.objects.filter(user=user_profile)
    post_len = len(post)
    listing_len = len(listings)

    return render(request, 'landing/dashboard.html', {'listing_len': listing_len, 'post_len': post_len, 'post': post, 'listings': listings, 'user_profile': user_profile,  'user_objects': user_objects})


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
    user_objects = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)

    post = Post.objects.filter(user=user_profile)
    post_len = len(post)
    return render(request, 'landing/podcast.html', {'post': post, 'post_len': post_len, 'user_profile': user_profile,  'user_objects': user_objects})


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
            return redirect('social:login')
    else:
        return render(request, "landing/login.html")


"""def register(request):
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
                messages.info(request, 'Eamil already registered')
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
                return redirect('social:profile')
        else:
            messages.info(request, 'password not matching')
            return redirect('social:register')
        return redirect('/')

    else:
        return render(request, 'landing/signup.html')"""

# Register a user


def validate_password(password):
    password_validators = [
        password_validation.MinimumLengthValidator(8),
        password_validation.CommonPasswordValidator(),
        password_validation.NumericPasswordValidator(),

    ]

    try:
        password_validation.validate_password(password, password_validators)
    except ValidationError as e:
        return str(e)
    return ''


def validate_username(username):
    if User.objects.filter(username=username).exists():
        return 'Username is already taken'
    return ''


def validate_email(email):
    if User.objects.filter(email=email).exists():
        return 'Email is already registered'
    return ''


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Validate fields
        username_error = validate_username(username)
        email_error = validate_email(email)
        password_error = validate_password(password)

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('social:register')

        if username_error:
            messages.error(request, username_error)
            return redirect('social:register')

        if email_error:
            messages.error(request, email_error)
            return redirect('social:register')

        if password_error:
            messages.error(request, password_error)
            return redirect('social:register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create profile
        Profile.objects.create(user=user)

        messages.success(request, 'Registration successful')
        return redirect('social:login')

    else:
        return render(request, 'landing/signup.html')


@ login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('social:login')
