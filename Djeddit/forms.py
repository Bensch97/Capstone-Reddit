from django import forms
from .models import Subreddit

class SubredditForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class PostForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['subreddit'].choices = [(sub.id, sub.name) for sub in Subreddit.objects.all()]

    content = forms.CharField(max_length=500)
    subreddit = forms.ChoiceField()