# Generated by Django 4.1 on 2024-02-12 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flick_seeker', '0009_alter_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Bio'),
        ),
    ]
