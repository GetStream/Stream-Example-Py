from django.core.management.base import BaseCommand
from django_stream.feed_managers import feed_manager
from django_stream import Follow
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        admin = get_user_model().objects.get(username="admin")
        Follow.objects.create(user=admin, target=admin)
        feed_manager.follow_user(admin, admin)
