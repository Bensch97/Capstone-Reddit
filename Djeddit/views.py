import datetime
import re
import calendar

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
from Djeddit.forms import SignupForm, LoginForm, SubredditForm, PostForm, CommentForm, BioForm
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
    user_post_upvotes, user_post_downvotes = (
        get_user_votes(request, all_entries)
    )

    data = {
        'posts': all_entries,
        'user_post_upvotes': user_post_upvotes,
        'user_post_downvotes': user_post_downvotes,
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


def bio_view(request, user):
    html = 'bio.html'
    current_user = Profile.objects.get(username=user)
    if request.method == 'POST':
        form = BioForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data
            current_user.bio = content['bio']
            current_user.save()
            print(current_user.bio)
            return HttpResponseRedirect('/u/{}/'.format(current_user.username))
    else:
        form = BioForm()
    return render(request, html, {'form': form, 'user': current_user})


def post_view(request, subreddit=None):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data
            post_to_subreddit_id = content['subreddit']
            subreddit = Subreddit.objects.get(pk=post_to_subreddit_id)
            print('subreddit_name', subreddit.name)
            redirect_to = subreddit.name
            Post.objects.create(
                title=content['title'],
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


def delete_comment_view(request, post, comment):
    Comment.objects.get(id=comment).delete()
    return HttpResponseRedirect('/p/{}/'.format(post))


def individual_post_view(request, post):
    current_user = Profile.objects.get(user=request.user)
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
    user_post_upvotes, user_post_downvotes = get_user_votes(
        request,
        Post.objects.filter(id=post)
    )
    user_comment_upvotes, user_comment_downvotes = get_user_votes(
        request,
        comments,
    )
    data = {
        'post': post_obj,
        'form': form,
        'comments': comments,
        'user_post_upvotes': user_post_upvotes,
        'user_post_downvotes': user_post_downvotes,
        'user_comment_upvotes': user_comment_upvotes,
        'user_comment_downvotes': user_comment_downvotes,
        'current_user': current_user
    }
    print(data)
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

    user_post_upvotes, user_post_downvotes = get_user_votes(request, posts)

    data = {
        'subreddit': subreddit_obj,
        'posts': posts,
        'user_post_upvotes': user_post_upvotes,
        'user_post_downvotes': user_post_downvotes,
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
    current_user = Profile.objects.get(user=request.user)
    cakeday_info = re.findall(r'\d+', str(profile_obj.user.date_joined))
    year = int(cakeday_info[0])
    month = calendar.month_name[int(cakeday_info[1])]
    day = cakeday_info[2]
    if day[0] == 0:
        day = day[1:]
    cakeday = '{} {}, {}'.format(month, day, year)

    if profile_obj is not None:
        posts = Post.objects.filter(profile_id=profile_obj)
        comments = Comment.objects.filter(profile_id=profile_obj)
        user_post_upvotes, user_post_downvotes = get_user_votes(request, posts)
    else:
        posts = None
        comments = None
        user_post_upvotes = None
        user_post_downvotes = None
        return HttpResponse('u/{} does not exist yet'.format(author))

    data = {
        'profile': profile_obj,
        'cakeday': cakeday,
        'posts': posts,
        'comments': comments,
        'user_post_upvotes': user_post_upvotes,
        'user_post_downvotes': user_post_downvotes,
        'current_user': current_user
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
        if request.POST.get("post_id"):
            post = Post.objects.get(id=request.POST.get("post_id"))
            updated_score = post.calculate_vote_score
        elif request.POST.get("comment_id"):
            comment = Comment.objects.get(id=request.POST.get("comment_id"))
            updated_score = comment.calculate_vote_score
    data = {
        "success": "success",
        "vote_type": request.POST.get("upvote"),
        "target_id": (request.POST.get("post_id")
                      or request.POST.get("comment_id")),
        "username": request.POST.get("username"),
        "updated_score": updated_score
    }
    print(data)
    return JsonResponse(data)
