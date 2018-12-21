from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
from .forms import *


def signup_view(request):
    form = SignupForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], 
            data['email'], 
            data['password']
        )
        Profile.objects.create(
            user = user,
            username = data['username'],
            karma = 0
        )
        login(request, user)
        return HttpResponseRedirect(reverse('Front Page'))
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = LoginForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('Front Page'))
    return render(request, 'login.html', {'form': form})


def front_page_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data
            temp_subreddit = Subreddit.objects.get(pk=1)
            
            Post.objects.create(
                content = content,
                vote_count = 0,
                profile_id = request.user.profile,
                subreddit_id = temp_subreddit
            )
            return HttpResponseRedirect('/thanks/')

    else:
        form = PostForm()

    return render(request, 'front_page.html', {'form': form})



@login_required
def create_subreddit_view(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Subreddit.objects.create(
                name = data['name'],
                created_at = timezone.now(),
                description = data['description'],
                created_by = Profile.objects.filter(user=request.user).first()
            )
    else:
        form = SubredditForm()
    return render(request, 'create_subreddit.html', {'form': form})


def thanks_view(request):
    return HttpResponse('Thanks')