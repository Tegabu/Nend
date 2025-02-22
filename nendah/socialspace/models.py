from email.mime import image
from email.policy import default
import unicodedata
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime
import uuid


User = get_user_model()

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(null=True)
    bio = models.TextField(blank=False)
    profileimg = models.ImageField(
        upload_to='profile_images', default='person.png')
    phone = models.IntegerField(default='0')

    def __str__(self):
        return self.user.username


class profile_pic(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_owner_pp(self):
        return self.author.profile.image.url


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=_MAX_LENGTH, blank=True, default="")
    post_date = models.DateTimeField(default=datetime.now)
    num_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class likepost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class product(models.Model):
    name = models.CharField(max_length=100)
    prodesc = models.TextField(max_length=_MAX_LENGTH, blank=False)
    pic = models.ImageField(upload_to='post_images')
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Host(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=False,
                            blank=False, default=None)
    location = models.CharField(
        max_length=100, null=False, blank=False, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    charge = models.DecimalField(
        max_digits=6, decimal_places=2, blank=False, default=None)
    img = models.ImageField(null=False, blank=False,
                            upload_to='post_images')

    def __str__(self):
        return self.name


class Listing(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='listing')
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    charge = models.FloatField()
    img = models.ImageField(null=False, blank=False,
                            upload_to='listing_images')
    is_available = models.BooleanField(default=False)
    host_name = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='listing')

    def __str__(self):
        return self.name


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
