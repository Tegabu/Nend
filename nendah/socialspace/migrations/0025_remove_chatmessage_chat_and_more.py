# Generated by Django 4.1.1 on 2023-03-12 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialspace', '0024_rename_conversation_chatmessage_chat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='created_by',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]
