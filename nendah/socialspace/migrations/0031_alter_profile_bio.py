# Generated by Django 4.1.1 on 2023-04-12 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialspace', '0030_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(),
        ),
    ]
