# Generated by Django 4.1.1 on 2023-04-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialspace', '0025_remove_chatmessage_chat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_user',
            field=models.IntegerField(default=0),
        ),
    ]
