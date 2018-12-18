from django import model
from django.contrib.auth.models import User

class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    username = Charfield(max_length=30)
    bio = CharField(max_length=300)
    karma = IntergerField()
    subscriptions = models.ManyToMany('Subreddit')
    moderators = models.ManyToMany('Subreddit')
    

class Post(models.Model):
    content = CharField(max_length=1000)
    timestamp = DateTimeField(auto_now_add=True, blank=True)
    vote_count = IntergerField()
    profile_id = ForeignKey(Profile)
    subreddit_id = ForeignKey(Subreddit)

class Subreddit(models.Model):
    name = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True, blank=True)
    description = Charfield(max_length=500)
    created_by = ForeignKey(Profile)

class Comment(models.Model):
    content = CharField(max_length=1000)
    timestamp = DateTimeField(auto_now_add=True, blank=True)
    profile_id = ForeignKey(Profile)
    post_id = ForeignKey(Post)
    parent_id = IntergerField()


    