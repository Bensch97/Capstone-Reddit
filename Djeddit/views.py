import datetime

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.views import generic

from Djeddit.models import Profile, Subreddit, Post, Comment
from Djeddit.forms import SignupForm, LoginForm, SubredditForm, PostForm, CommentForm
from Djeddit.utils import handle_vote, get_user_votes


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
        send_mail('Thanks for creating your account!',
                  "Thank you for registering your account {}. We hope you enjoy Djeddit!"
                  .format(data['username']),
                  settings.EMAIL_HOST_USER,
                  [data['email']], fail_silently=False)
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
    all_entries = Post.objects.all().order_by('-vote_score')
    user_upvotes, user_downvotes = get_user_votes(request, all_entries)

    data = {
        'posts': all_entries,
        'user_upvotes': user_upvotes,
        'user_downvotes': user_downvotes,
    }
    return render(request, 'front_page.html', data)


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
    if request.method == 'POST':
        form = PostForm(None, request.POST)
        if form.is_valid():
            content = form.cleaned_data
            post_to_subreddit_id = content['subreddit']
            subreddit = Subreddit.objects.get(pk=post_to_subreddit_id)
            print('subreddit_name', subreddit.name)
            redirect_to = subreddit.name
            Post.objects.create(
                content=content['content'],
                vote_count=0,
                profile_id=request.user.profile,
                subreddit_id=subreddit,
            )
            return HttpResponseRedirect('/r/{}/'.format(redirect_to))

    else:

        if subreddit == None:
            form = PostForm()

        else:
            subreddit_object_for_form = Subreddit.objects.get(name=subreddit)
            form = PostForm(subreddit_object_for_form)

    return render(request, 'post_page.html', {'form': form})


def individual_post_view(request, post):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data
            Comment.objects.create(
                content=comment['content'],
                profile_id=Profile.objects.filter(user=request.user).first(),
                post_id=Post.objects.filter(id=post).first(),
                parent_id=1,
            )
            return HttpResponseRedirect('/p/{}/'.format(post))

    else:
        form = CommentForm
    html = 'post.html'
    post_obj = Post.objects.filter(id=post).first()
    comments = Comment.objects.filter(post_id=post_obj)
    user_upvotes, user_downvotes = get_user_votes(
        request,
        Post.objects.filter(id=post)
        )
    data = {
        'post': post_obj,
        'form': form,
        'comments': comments,
        'user_upvotes': user_upvotes,
        'user_downvotes': user_downvotes,
    }
    return render(request, html, data)


def subreddit_view(request, subreddit):
    html = 'subreddit.html'
    subreddit_obj = Subreddit.objects.get(name=subreddit)
    current_user = Profile.objects.get(user=request.user)
    subscriptions = current_user.subscriptions.all()

    if subreddit_obj is not None:
        posts = Post.objects.filter(
            subreddit_id=subreddit_obj
        ).order_by('-vote_score')
    else:
        posts = None
        return HttpResponse('r/{} does not exist yet'.format(subreddit))

    user_upvotes, user_downvotes = get_user_votes(request, posts)

    data = {
        'subreddit': subreddit_obj,
        'posts': posts,
        'user_upvotes': user_upvotes,
        'user_downvotes': user_downvotes,
        'subscriptions': subscriptions
    }

    return render(request, html, data)


def subscription_view(request, subreddit):
    current_user = Profile.objects.get(user=request.user)
    sub = Subreddit.objects.get(name=subreddit)
    current_user.subscriptions.add(sub)
    return HttpResponseRedirect('/r/{}/'.format(subreddit))


def unsubscription_view(request, subreddit):
    current_user = Profile.objects.get(user=request.user)
    sub = Subreddit.objects.get(name=subreddit)
    current_user.subscriptions.remove(sub)
    return HttpResponseRedirect('/r/{}/'.format(subreddit))


def profile_view(request, author):
    html = 'user_profile.html'
    profile_obj = Profile.objects.filter(username=author).first()

    if profile_obj is not None:
        posts = Post.objects.filter(profile_id=profile_obj)
        comments = Comment.objects.filter(profile_id=profile_obj)
        user_upvotes, user_downvotes = get_user_votes(request, posts)
    else:
        posts = None
        comments = None
        user_upvotes = None
        user_downvotes = None
        return HttpResponse('u/{} does not exist yet'.format(author))
   
    data = {
        'profile': profile_obj,
        'posts': posts,
        'comments': comments,
        'user_upvotes': user_upvotes,
        'user_downvotes': user_downvotes,
    }

    return render(request, html, data)


class ExploreView(generic.ListView):
    template_name = 'explore.html'
    context_object_name = 'subreddits'

    def get_queryset(self):
        return Subreddit.objects.all()


def ajax_vote(request):
    if request.POST:
        handle_vote(request)
        post = Post.objects.get(id=request.POST.get("post_id"))
        new_post_score = post.calculate_vote_score
    data = {
        "success": "success",
        "vote_type": request.POST.get("upvote"),
        "post_id": request.POST.get("post_id"),
        "username": request.POST.get("username"),
        "updated_score": new_post_score
    }
    return JsonResponse(data)
