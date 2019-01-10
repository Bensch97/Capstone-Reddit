from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User

from Djeddit import models
from Djeddit.utils import handle_vote, get_user_votes


class HelperTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.client.login(username='test', password='test')
        models.Profile.objects.create(
            user=self.user,
            username=self.user.username,
            email=self.user.email,
            karma=0
        )
        models.Subreddit.objects.create(
            name='TEST_SUB',
            description='DESCRIPTION',
            created_by=models.Profile.objects.get(user=self.user)

        )
        models.Post.objects.create(
            title='TEST_TITLE',
            content='TEST_CONTENT',
            vote_count=0,
            profile_id=models.Profile.objects.get(user=self.user),
            subreddit_id=models.Subreddit.objects.get(pk=1),
        )

    def test_get_user_votes(self):
        posts = models.Post.objects.all()
        request = self.factory.get('/')
        request.user = self.user
        self.assertEqual(get_user_votes(request, posts), ([], []))

    def test_handle_vote(self):
        data = {'upvote': 'upvote', 'post_id': '1'}
        request = self.factory.post('/', data)
        request.user = self.user
        self.assertEqual(handle_vote(request), 'foo')
