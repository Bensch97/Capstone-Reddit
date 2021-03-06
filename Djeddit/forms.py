from django import forms
from .models import Subreddit, Profile

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
            self.fields['subreddit'].choices = [(sub.id, sub.name) for sub in Subreddit.objects.all()]
        else:
            self.fields['subreddit'].choices = [(subreddit.id, subreddit.name)]
    
    title = forms.CharField(max_length=300)
    content = forms.CharField(widget=forms.Textarea)
    subreddit = forms.ChoiceField()


class CommentForm(forms.Form):
    content = forms.CharField(max_length=1000)

class ModeratorForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ModeratorForm, self).__init__(*args, **kwargs)

        self.fields['user'].choices = [(prof.id, prof.user) for prof in Profile.objects.all()]
        self.fields['subreddit'].choices = [(subreddit.id, subreddit.name) for subreddit in Subreddit.objects.all() if subreddit.created_by == user]

    subreddit = forms.ChoiceField()
    user = forms.ChoiceField()

class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)

class ReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class OrderForm(forms.Form):
    def __init__(self, order_choice, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.initial['order'] = 'Best'


    ORDER_CHOICES = (
        ('BEST', 'Best'),
        ('NEW', 'New'),
    )

    order = forms.ChoiceField(choices=ORDER_CHOICES, label="",
                              widget=forms.Select(), 
                              required=True)
