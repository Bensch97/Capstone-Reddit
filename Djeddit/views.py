from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from .forms import *


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