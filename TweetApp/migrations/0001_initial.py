# Generated by Django 4.1.1 on 2022-09-20 12:46

import TweetApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(related_name='liked_tweets', to=settings.AUTH_USER_MODEL)),
                ('retweets', models.ManyToManyField(related_name='retweeted_tweets', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TweetMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to=TweetApp.models.upload_media_path)),
                ('tweet', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='TweetApp.tweet')),
            ],
        ),
    ]