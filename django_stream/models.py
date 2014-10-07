from core.feed_managers import stream_client
from django.conf import settings
from django.db import models
from django.utils.timezone import make_naive
import pytz
from django.template.defaultfilters import slugify
from django_stream import model_managers


class Activity(models.Model):
    # which feed to push this activity to
    feeds = ['user']
    # Set to False to temporarily/permanently disable posting
    broadcast_activity = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def extra_activity_data(self):
        '''
        Use this hook to setup extra activity data
        '''
        pass
    
    @property
    def verb(self):
        model_name = slugify(self.__class__.__name__)
        return model_name
    
    @property
    def foreign_id(self):
        app_label = self.__class__.__module__.split('.')[-2]
        model_name = slugify(self.__class__.__name__)
        foreign_id = '%s:%s:%s' % (app_label, model_name, self.pk)
        return foreign_id
    
    @property
    def actor_id(self):
        return self.user_id
    
    @property
    def time(self):
        return make_naive(self.created_at, pytz.utc)
    
    @property
    def notify(self):
        pass
    
    def create_activity(self):
        extra_data = self.extra_activity_data()
        if not extra_data:
            extra_data = {}
        
        to = self.notify
        if to:
            extra_data['to'] = to
        
        activity = dict(
            actor=self.actor_id,
            verb=self.verb,
            object=self.pk,
            foreign_id=self.foreign_id,
            time=self.time,
            **extra_data
        )
        return activity
    
    def save(self, *args, **kwargs):
        created = not self.id
        result = models.Model.save(self, *args, **kwargs)
        self.post_save(created)
        return result
    
    def delete(self, *args, **kwargs):
        result = models.Model.delete(self, *args, **kwargs)
        self.post_delete()
        return result
    
    def post_save(self, created, **kwargs):
        instance = self
        if getattr(instance, 'broadcast_activity', None) == False:
            return
        activity = instance.create_activity()
        if created:
            print 'post save', created
            result = self.add_user_activity(activity['actor'], activity)
        elif instance.deleted_at:
            result = self.remove_user_activity(activity['actor'], activity)
        return result

    def post_delete(self, **kwargs):
        instance = self
        if getattr(instance, 'broadcast_activity', None) == False:
            return
        activity = instance.create_activity()
        return self.remove_user_activity(activity['actor_id'], activity)
        
    def add_user_activity(self, user_id, activity):
        feed = stream_client.feed('user:%s' % user_id)
        result = feed.add_activity(activity)
        return result

    def remove_user_activity(self, user_id, activity):
        feed = stream_client.feed('user:%s' % user_id)
        result = feed.remove_activity(foreign_id=activity['foreign_id'])
        return result
    
    def filter_to(self, current_user, to):
        '''
        Remove the current user from to and make the list unqiue
        '''
        to = set(to)
        to.discard(current_user.id)
        to = list(to)
        return to
    
    class Meta:
        abstract = True


class Follow(Activity):
    '''
    A simple table mapping who a user is following. 
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='following_set')
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='follower_set')
    
    # a bit of tracking
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    objects = model_managers.FollowManager()
    
    def delete(self, *args, **kwargs):
        self.unfollow_user()
        
    def save(self, *args, **kwargs):
        created = not self.id
        result = Activity.save(self, *args, **kwargs)
        if created and not self.deleted_at:
            self.follow_user()
        return result
        
    def add_notification(self, user_id, activity):
        feed = stream_client.feed('notification:%s' % user_id)
        result = feed.add_activity(activity)
        return result
        
    def _set_follow_user(self, user_id, target_id, method='follow'):
        '''
        Makes the aggregated:user_id and flat:user_id
        follow
        user:target_id
        '''
        target_feed_id = 'user:%s' % target_id
        results = []
        for feed_slug in ['aggregated', 'flat']:
            feed = stream_client.feed('%s:%s' % (feed_slug, user_id))
            operation = getattr(feed, method)
            result = operation(target_feed_id)
            results.append(result)
        return result

    def follow_user(self):
        result = self._set_follow_user(
            self.user_id, self.target_id, method='follow')
        # send a notification to the person which got followed
        activity = self.create_activity()
        self.add_notification(self.target_id, activity)

        return result

    def unfollow_user(self):
        return self._set_follow_user(self.user_id, self.target_id, method='unfollow')

    def extra_activity_data(self):
        # extra data to denormalize
        return dict(follow_target=self.target_id)

    class Meta:
        ordering = ['-id']
        
        