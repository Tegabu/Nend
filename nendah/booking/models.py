from django.db import models
from email.mime import image
from email.policy import default
import unicodedata
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime
import uuid

from socialspace.models import Listing

User = get_user_model()
# Create your models here.


class Chat(models.Model):
    listing = models.ForeignKey(
        Listing, related_name='chat', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='created_messages', on_delete=models.CASCADE)
