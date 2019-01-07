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
    def __init__(self, subreddit=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if subreddit == None:
            print('none')
            self.fields['subreddit'].choices = [(sub.id, sub.name) for sub in Subreddit.objects.all()]
        else:
            print('getting choices', subreddit.id, subreddit.name)
            self.fields['subreddit'].choices = [(subreddit.id, subreddit.name)]
    
    title = forms.CharField(max_length=300)
    content = forms.CharField(widget=forms.Textarea)
    subreddit = forms.ChoiceField()


class CommentForm(forms.Form):
    content = forms.CharField(max_length=1000)


class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)