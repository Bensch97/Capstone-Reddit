from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    bio = models.CharField(max_length=300)
    karma = models.IntegerField()
    subscriptions = models.ManyToManyField('Subreddit', related_name='sub_subscriptions')
    moderators = models.ManyToManyField('Subreddit', related_name='mod_subscriptions')


class Subreddit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Post(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    vote_count = models.IntegerField()
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subreddit_id = models.ForeignKey(Subreddit, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_id = models.IntegerField()
