from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('upload', views.upload, name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('profile', views.profile, name="profile"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('duka', views.duka, name="duka"),
    path('settings', views.settings, name="settings"),
    path('podcast', views.podcast, name="podcast"),
    path('articles', views.articles, name="articles"),
    path('chat', views.chat, name="chat"),
    path('bookings', views.booking, name="bokings"),


]
