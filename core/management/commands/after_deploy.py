from django.core.management.base import BaseCommand
from core.feed_managers import manager
from core.models import Follow
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        admin = get_user_model().objects.get(username="admin")
        follow = Follow.objects.create(user=admin, target=admin)
        manager.follow_user(follow)
