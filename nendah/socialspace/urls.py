from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('base/<str:pk>', views.base, name='base'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('upload', views.upload, name='upload'),
    path('new_listing', views.new, name='new_listing'),
    path('addlisting', views.addlisting, name='addlisting'),
    path('like-post', views.like_post, name='like-post'),
    path('profile', views.settings, name="profile"),
    path('follow', views.follow, name="follow"),
    path('user/<str:pk>', views.user, name="user"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name="logout"),
    path('duka', views.duka, name="duka"),
    path('settings', views.settings, name="settings"),
    path('podcast', views.podcast, name="podcast"),

    path('cart', views.cart, name="cart"),
    path('find', views.find, name="find"),
    path('bookings', views.bookings, name="bookings"),
    path('feed', views.feed, name="feed"),
    path('search', views.search_bar, name="search"),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/editlisting/', views.editlisting, name="editlisting"),
    path('dashboard', views.duka, name="dashboard"),




]
