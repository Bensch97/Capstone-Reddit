from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.utils import timezone

from Djeddit.models import Profile, Subreddit, Post
from Djeddit.forms import SignupForm, LoginForm, SubredditForm


def signup_view(request):
    form = SignupForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        Profile.objects.create(
            user=user,
            username=data['username'],
            karma=0
        )
        login(request, user)
        return HttpResponseRedirect(reverse('Front Page'))
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = LoginForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('Front Page'))
    return render(request, 'login.html', {'form': form})


def front_page_view(request):
    return render(request, 'front_page.html')


@login_required
def create_subreddit_view(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Subreddit.objects.create(
                name=data['name'],
                created_at=timezone.now(),
                description=data['description'],
                created_by=Profile.objects.filter(user=request.user).first()
            )
            return HttpResponse('Successfully created a subreddit')
    else:
        form = SubredditForm()
    return render(request, 'create_subreddit.html', {'form': form})


def subreddit_view(request, subreddit):
    html = 'subreddit.html'
    # TODO database is allowing duplicate subreddits.This is a workaround to test if data can appear.
    # subreddit_obj = Subreddit.objects.get(name=subreddit)
    subreddit_obj = Subreddit.objects.filter(name=subreddit).first()

    if subreddit_obj is not None:
        posts = Post.objects.filter(subreddit_id=subreddit_obj)
    else:
        posts = None
        return HttpResponse('r/{} does not exist yet'.format(subreddit))
    data = {
        'subreddit': subreddit_obj,
        'posts': posts
    }
    if request.method == 'POST':
        pass
        # TODO add functionality for upvotes/downvotes
    else:
        print(data)

    return render(request, html, data)


def explore_view(request):
    html = 'explore.html'
    subreddits = Subreddit.objects.all()
    data = {
        'subreddits': subreddits
    }

    return render(request, html, data)
