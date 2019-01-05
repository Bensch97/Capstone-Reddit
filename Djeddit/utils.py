from Djeddit.models import Profile, Post


def handle_vote(request):
    """
    Takes in request obj and handles upvoting and downvoting via POST req.
    """
    current_user_profile = Profile.objects.get(user__id=request.user.id)
    post_id = request.POST.get('post_id')
    targeted_post = Post.objects.get(id=post_id)

    if request.POST.get('upvote'):
        # user has already upvoted
        if targeted_post.votes.exists(current_user_profile.user.id):
            targeted_post.votes.delete(current_user_profile.user.id)
        # user has not voted or user has already downvoted
        else:
            targeted_post.votes.up(current_user_profile.user.id)
    elif request.POST.get('downvote'):
        # user has already upvoted
        if targeted_post.votes.exists(current_user_profile.user.id):
            targeted_post.votes.down(current_user_profile.user.id)
        # user has already downvoted
        elif targeted_post.votes.get(current_user_profile.user.id):
            targeted_post.votes.delete(current_user_profile.user.id)
        # user has not voted
        else:
            targeted_post.votes.down(current_user_profile.user.id)
