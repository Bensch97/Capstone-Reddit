import datetime

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.utils import timezone

from Djeddit.models import Profile, Subreddit, Post
from Djeddit.forms import SignupForm, LoginForm, SubredditForm, PostForm


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
    all_entries = Post.objects.all().order_by('timestamp')
    entry_content_author = []
    for entry in all_entries:
        user_who_posted = entry.profile_id.username
        subreddit = entry.subreddit_id.name
        vote_count = entry.vote_count
        timestamp = entry.timestamp

        post_tuple = (entry.content, user_who_posted, subreddit, vote_count, timestamp)
        entry_content_author.append(post_tuple)

    return render(request, 'front_page.html', {'posts': entry_content_author})


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


def thanks_view(request):
    return HttpResponse('Thanks')


def post_view(request, subreddit=None):
    print('subreddit', subreddit)
    if request.method == 'POST':
        form = PostForm(None, request.POST)
        if form.is_valid():
            content = form.cleaned_data
            post_to_subreddit_id = content['subreddit']
            print('subreddit id', post_to_subreddit_id)
            subreddit = Subreddit.objects.get(pk=post_to_subreddit_id)
            Post.objects.create(
                content = content['content'],
                vote_count = 0,
                profile_id = request.user.profile,
                subreddit_id = subreddit,
            )
            return HttpResponseRedirect('/thanks/')
    
    # Perhaps we can delete this?
    else:

        if subreddit == None:
            print('none')
            form = PostForm()

        else:
            subreddit_object_for_form = Subreddit.objects.get(name=subreddit)
            print('subreddit for form', subreddit_object_for_form.id)
            form = PostForm(subreddit_object_for_form)

    return render(request, 'post_page.html', {'form': form})


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
        pass
        # print('data', data)

    return render(request, html, data)


def profile_view(request, author):
    html = 'user_profile.html'
    profile_obj = Profile.objects.filter(username=author).first()

    if profile_obj is not None:
        posts = Post.objects.filter(profile_id=profile_obj)
    else:
        posts = None
        return HttpResponse('u/{} does not exist yet'.format(author))
    data = {
        'profile': profile_obj,
        'posts': posts
    }
    if request.method == 'POST':
        pass
        # TODO add uvote/downvote fuctionality
    
    return render(request, html, data)

def explore_view(request):
    html = 'explore.html'
    subreddits = Subreddit.objects.all()
    data = {
        'subreddits': subreddits
    }

    return render(request, html, data)
