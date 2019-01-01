from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import F

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
    all_entries = Post.objects.all()
    print(all_entries)
    for post in all_entries:
        print(post)
    return render(request, 'front_page.html', {'posts': all_entries})


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


def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data
            post_to_subreddit_id = content['subreddit']
            subreddit = Subreddit.objects.get(pk=post_to_subreddit_id)
            print(subreddit)
            Post.objects.create(
                content=content['content'],
                vote_count=0,
                profile_id=request.user.profile,
                subreddit_id=subreddit
            )
            return HttpResponseRedirect('/thanks/')

    else:
        form = PostForm()

    return render(request, 'post_page.html', {'form': form})


def subreddit_view(request, subreddit):
    html = 'subreddit.html'
    subreddit_obj = Subreddit.objects.get(name=subreddit)

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
        print(request.POST)
        post_id = request.POST.get('post_id')
        targeted_post = Post.objects.get(pk=post_id)
        if request.POST.get('upvote'):
            targeted_post.vote_count = F('vote_count') + 1
            targeted_post.save()
        elif request.POST.get('downvote'):
            targeted_post.vote_count = F('vote_count') - 1
            targeted_post.save()
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
