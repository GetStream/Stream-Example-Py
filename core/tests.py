from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client
from django.test.testcases import TestCase
from django_stream.models import Follow
from mock import Mock, patch


class PinTestCase(TestCase):
    fixtures = ['test_data']
    
    def setUp(self):
        TestCase.setUp(self)
        from core.models import Item
        print Item.objects.all().count()
        self.client = Client()
        self.auth_client = Client()
        response = self.auth_client.login(username='admin', password='admin')
        self.assertTrue(response)
        self.admin = get_user_model().objects.get(username='admin')
        self.bogus = get_user_model().objects.get(username='bogus')
        
    def test_pin(self):
        pin_url = reverse('pin')
        data = dict(message='test', board_name='My favourite things', item=5, influencer=1)
        
        with patch('stream.feed.Feed.add_activity') as mocked:
            response = self.auth_client.post(pin_url, data)
            print mocked.mock_calls
            self.assertEqual(mocked.call_count, 1)

    def test_follow(self):
        with patch('stream.feed.Feed.follow') as mocked:
            follow = Follow.objects.follow(self.bogus, self.admin)
            print mocked.mock_calls
            # we have 2 feeds
            self.assertEqual(mocked.call_count, 2)