from django.test import Client
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase
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
        
    def test_pin(self):
        pin_url = reverse('pin')
        data = dict(message='test', board_name='My favourite things', item=5, influencer=1)
        
        with patch('stream.feed.Feed.add_activity') as mocked:
            response = self.auth_client.post(pin_url, data)
            print mocked.mock_calls
            self.assertEqual(mocked.call_count, 1)
