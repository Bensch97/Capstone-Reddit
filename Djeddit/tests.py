from django.test import TestCase, Client
from Djeddit import models
from Djeddit.utils import handle_vote, get_user_votes


class HelperTestCase(TestCase):
        def setUp(self):
            c = Client()

        def test_get_user_votes(self):
            get_user_votes()

        def test_handle_vote(self):
            pass
