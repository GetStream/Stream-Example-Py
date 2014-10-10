from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager


class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        abstract = True


class Item(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='items')
    source_url = models.TextField()
    message = models.TextField(blank=True, null=True)
    pin_count = models.IntegerField(default=0)


class Pin(Activity, BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)
    influencer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='influenced_pins')
    message = models.TextField(blank=True, null=True)

    @classmethod
    def related_models(cls):
        return ['user', 'item']

    @property
    def extra_activity_data(self):
        return dict(item_id=self.item_id)


class Follow(Activity, BaseModel):
    '''
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='follower_set')

    @classmethod
    def related_models(cls):
        return ['user', 'target']


def follow_feed(sender, instance, created, **kwargs):
    if created:
        feed_manager.follow_user(instance.user_id, instance.target_id)


def unfollow_feed(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user_id, instance.target_id)


post_save.connect(follow_feed, sender=Follow)
post_delete.connect(unfollow_feed, sender=Follow)

