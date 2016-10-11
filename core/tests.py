from __future__ import print_function
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client
from django.test.testcases import TestCase
from core.models import Follow
from mock import patch

from stream_django.feed_manager import feed_manager


class PinTestCase(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        TestCase.setUp(self)
        from core.models import Item
        print(Item.objects.all().count())
        self.client = Client()
        self.auth_client = Client()
        response = self.auth_client.login(username='admin', password='admin')
        self.assertTrue(response)
        self.admin = get_user_model().objects.get(username='admin')
        self.bogus = get_user_model().objects.get(username='bogus')

    def tearDown(self):
        feed_manager.disable_model_tracking()

    def test_pin(self):
        pin_url = reverse('pin')
        data = dict(message='test', board_name='My favourite things', item=5,
                    influencer=1)

        feed_manager.enable_model_tracking()

        with patch('stream.feed.Feed.add_activity') as mocked:
            self.auth_client.post(pin_url, data)
            self.assertEqual(mocked.call_count, 1)

    def test_follow(self):
        with patch('stream.feed.Feed.follow') as mocked:
            Follow.objects.create(user=self.bogus, target=self.admin)
            print(mocked.mock_calls)
            # we have 2 feeds
            self.assertEqual(mocked.call_count, 2)
