from django.db import models
from django.conf import settings
from django.utils.timezone import make_naive
import pytz


class BaseModel(models.Model):

    class Meta:
        abstract = True


class Item(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to='items')
    source_url = models.TextField()
    message = models.TextField(blank=True, null=True)
    pin_count = models.IntegerField(default=0)


class Board(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()


class Pin(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)
    board = models.ForeignKey(Board)
    influencer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='influenced_pins')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def create_activity(self):
        activity = dict(
            actor=self.user_id,
            verb='pin',
            object=self.id,
            target=self.influencer_id,
            time=make_naive(self.created_at, pytz.utc),
            foreign_id='pin:%s' % self.id,
            item_id=self.item_id
        )
        return activity


class Follow(BaseModel):
    '''
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)
