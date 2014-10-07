
from django.db import models
import datetime


class FollowManager(models.Manager):
    def follow(self, user, target):
        follow, created = self.get_or_create(user=user, target=target)
        if not created and follow.deleted_at:
            follow.deleted_at = None
            follow.save()
        return follow
    
    def unfollow(self, user, target):
        follow, created = self.get_or_create(user=user, target=target)
        if not follow.deleted_at:
            follow.deleted_at = datetime.datetime.now()
            follow.save()
        return follow