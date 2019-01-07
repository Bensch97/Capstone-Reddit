from Djeddit.models import Profile, Post, Comment


def handle_vote(request):
    """
    Takes in request obj and handles upvoting and downvoting via POST req.
    """
    current_user_profile = Profile.objects.get(user__id=request.user.id)
    targeted_id = request.POST.get('post_id') or request.POST.get('comment_id')
    if request.POST.get('comment_id'):
        target_comment = Post.objects.filter(id=request.POST.get('comment_id'))
    elif request.POST.get('post_id'):
        target_post = Post.objects.filter(id=request.POST.get('post_id'))

  
    if request.POST.get('post_id'):
        targeted_post = Post.objects.get(id=targeted_id)
        targeted_user_id = Post.objects.values_list('profile_id', flat=True).get(id=targeted_id)
        targeted_user = Profile.objects.get(id=targeted_user_id)
    elif request.POST.get('comment_id'):
        targeted_post = Comment.objects.get(id=targeted_id)
        targeted_user_id = Post.objects.values_list('profile_id', flat=True).get(id=targeted_id)
        targeted_user = Profile.objects.get(id=targeted_user_id)

    if request.POST.get('upvote'):
        # user has already upvoted
        if targeted_post.votes.exists(current_user_profile.user.id):
            targeted_post.votes.delete(current_user_profile.user.id)
            targeted_user.karma = targeted_user.karma - 1
            targeted_user.save()
        # user has not voted or user has already downvoted
        else:
            targeted_post.votes.up(current_user_profile.user.id)
            targeted_user.karma = targeted_user.karma + 1
            targeted_user.save()
    elif request.POST.get('downvote'):
        # user has already upvoted
        if targeted_post.votes.exists(current_user_profile.user.id):
            targeted_post.votes.down(current_user_profile.user.id)
            targeted_user.karma = targeted_user.karma - 2
            targeted_user.save()
        # user has already downvoted
        elif targeted_post.votes.get(current_user_profile.user.id):
            targeted_post.votes.delete(current_user_profile.user.id)
            targeted_user.karma = targeted_user.karma + 1
            targeted_user.save()
        # user has not voted
        else:
            targeted_post.votes.down(current_user_profile.user.id)
            targeted_user.karma = targeted_user.karma - 1
            targeted_user.save()


def get_user_votes(request, posts):
    """
    Takes in request object and Post queryset object
    and returns tuple of lists with post ids
    that user has upvoted and downvoted respectively
    """
    user_upvotes = []
    user_downvotes = []
    for p in posts:
        if p.votes.exists(request.user.id, action=0):
            user_upvotes.append(p.id)
        elif p.votes.exists(request.user.id, action=1):
            user_downvotes.append(p.id)
    return (user_upvotes, user_downvotes)