from django.db import models
from django.contrib.auth.models import User

from vote.models import VoteModel


class Subreddit(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey('Profile', on_delete=models.CASCADE)
    moderators = models.ManyToManyField(
        'Profile',
        related_name='mod_subscriptions',
        blank=True
    )
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    bio = models.CharField(max_length=300)
    karma = models.IntegerField()
    subscriptions = models.ManyToManyField(
        'Subreddit',
        related_name='sub_subscriptions',
        blank=True
    )
    

    def __str__(self):
        return self.user.username


class Post(VoteModel, models.Model):
    title = models.CharField(max_length=300, default='No Title')
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    vote_count = models.IntegerField()
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subreddit_id = models.ForeignKey(Subreddit, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Comment(VoteModel, models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_id = models.IntegerField()

    def __str__(self):
        return self.content


class Reply(VoteModel, models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent_id= models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.content