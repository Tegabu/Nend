from django.urls import path
from . import views

urlpatterns = [
    path('base/<str:pk>', views.base, name='base'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('upload', views.upload, name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('profile', views.profile, name="profile"),
    path('follow', views.follow, name="follow"),
    path('user/<str:pk>', views.user, name="user"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('duka', views.duka, name="duka"),
    path('settings', views.settings, name="settings"),
    path('podcast', views.podcast, name="podcast"),
    path('cart', views.cart, name="cart"),
    path('chat', views.chat, name="chat"),
    path('bookings', views.bookings, name="bookings"),
    path('feed', views.feed, name="feed"),


]
