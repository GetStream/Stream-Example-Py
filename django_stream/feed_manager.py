from activity import Activity
from django.db.models.signals import class_prepared
from django.db.models.signals import post_delete, post_save
from client import stream_client


#TODO: make this configurable via Django Settings
DEFAULT_PERSONAL_FEED = 'user'
DEFAULT_USER_FEEDS = {
    'flat':'flat',
    'aggregated':'aggregated'
}


class FeedManager(object):

    def __init__(self):
        self.content_type_models = {}
        self.personal_feed = DEFAULT_PERSONAL_FEED
        self.user_feeds = DEFAULT_USER_FEEDS

    def get_personal_feed(self, user_id, feed_type=None):
        if feed_type is None:
            feed_type = self.personal_feed
        feed = stream_client.feed('%s:%s' % (feed_type, user_id))
        return feed

    def get_actor_feed(self, instance=None):
        if instance.author_feed is not None:
            return instance.author_feed
        else:
            return self.personal_feed

    def follow_user(self, user_id, target_user_id):
        user_feeds = self.get_user_feeds(user_id)
        target_feed = self.get_personal_feed(target_user_id)
        for feed in user_feeds:
            self.unfollow_feed(target_feed)

    def unfollow_user(self, user_id, target_user_id):
        user_feeds = self.get_user_feeds(user_id)
        target_feed = self.get_personal_feed(target_user_id)
        for feed in user_feeds:
            self.unfollow_feed(target_feed)

    def get_feed(self, feed, user_id):
        return stream_client.feed('%s:%s' % (feed, user_id))

    def get_user_feeds(self, user_id):
        feeds = {}
        for feed in self.user_feeds:
            feeds[feed] = self.get_feed(feed, user_id)
        return feeds

    def activity_created(self, sender, instance, created, **kwargs):
        if created:
            activity = instance.create_activity()
            feed_type = self.get_actor_feed(instance)
            feed = self.get_feed(feed_type, instance.actor_id)
            result = feed.add_activity(activity)
            return result

    def activity_delete(self, sender, instance, **kwargs):
        feed_type = self.get_actor_feed(instance)
        feed = self.get_feed(feed_type, instance.actor_id)
        result = feed.remove_activity(foreign_id=instance.foreign_id)
        return result

    def bind_model(self, sender, **kwargs):
        if issubclass(sender, (Activity, )):
            self.content_type_models[sender.content_type()] = sender
            post_save.connect(self.activity_created, sender=sender)
            post_delete.connect(self.activity_delete, sender=sender)


feed_manager = FeedManager()
class_prepared = class_prepared.connect(feed_manager.bind_model)
