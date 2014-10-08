from activity import Activity
from client import stream_client
from collections import defaultdict
from django.db.models.signals import class_prepared
from django.db.models.signals import post_delete, post_save
from django.db.models.loading import get_model
import operator


#TODO: make this configurable via Django Settings
DEFAULT_PERSONAL_FEED = 'user'
DEFAULT_USER_FEEDS = {
    'flat':'flat',
    'aggregated':'aggregated'
}


def combine_dicts(a, b, op=operator.add):
    return dict(a.items() + b.items() +
        [(k, op(a[k], b[k])) for k in set(b) & set(a)])


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
        for feed in user_feeds.values():
            feed.follow(target_feed.feed_id)

    def unfollow_user(self, user_id, target_user_id):
        user_feeds = self.get_user_feeds(user_id)
        target_feed = self.get_personal_feed(target_user_id)
        for feed in user_feeds.values():
            feed.unfollow(target_feed.feed_id)

    def get_feed(self, feed, user_id):
        return stream_client.feed('%s:%s' % (feed, user_id))

    def get_user_feeds(self, user_id):
        feeds = {}
        for feed in self.user_feeds:
            feeds[feed] = self.get_feed(feed, user_id)
        return feeds

    def enrich_aggregated_activities(self, activities):
        fields = ['actor', 'object']
        references = {}
        for activity in activities:
            references = combine_dicts(references, self._collect_references(activity['activities'], fields))
        objects = self._fetch_objects(references)
        for activity in activities:
            self._inject_objects(activity['activities'], objects, fields)
        return activities

    def enrich_activities(self, activities):
        fields = ['actor', 'object']
        references = self._collect_references(activities, fields)
        objects = self._fetch_objects(references)
        self._inject_objects(activities, objects, fields)
        return activities

    def _collect_references(self, activities, fields):
        model_references = defaultdict(list)
        for activity in activities:
            for field in fields:
                if field in activity:
                    f_ct, f_id = activity[field].split(':')
                    model_references[f_ct].append(f_id)
        return model_references

    def _fetch_objects(self, references):
        objects = defaultdict(list)
        for content_type, ids in references.items():
            model = get_model(*content_type.split('.'))
            objects[content_type] = model.objects.in_bulk(set(ids))
        return objects

    def _inject_objects(self, activities, objects, fields):
        for activity in activities:
            for field in fields:
                if field in activity:
                    f_ct, f_id = activity[field].split(':')
                    activity[field] = objects[f_ct][int(f_id)]

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
            post_save.connect(self.activity_created, sender=sender)
            post_delete.connect(self.activity_delete, sender=sender)


feed_manager = FeedManager()
class_prepared = class_prepared.connect(feed_manager.bind_model)
