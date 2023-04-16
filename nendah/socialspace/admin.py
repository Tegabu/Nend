from django.contrib import admin
from .models import Profile, Post, likepost, product, Category, Host, FollowersCount, Listing

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(likepost)
admin.site.register(product)
admin.site.register(Category)
admin.site.register(Host)
admin.site.register(FollowersCount)
admin.site.register(Listing)
