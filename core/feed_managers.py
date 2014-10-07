from django.conf import settings
import os
import stream


if settings.STREAM_API_KEY and settings.STREAM_API_SECRET:
    stream_client = stream.connect(
        settings.STREAM_API_KEY, settings.STREAM_API_SECRET)
else:
    stream_client = stream.connect()


if os.environ.get('STREAM_URL') is None and not(settings.STREAM_API_KEY and settings.STREAM_API_SECRET):
    raise KeyboardInterrupt('Stream credentials are not set in your settings')


class PinManager(object):
    feed_types = dict(
        flat='flat',
        aggregated='aggregated'
    )

    def get_feeds(self, user_id):
        feeds = {}
        for feed in self.feed_types:
            feeds[feed] = stream_client.feed('%s:%s' % (feed, user_id))
        return feeds

    def get_user_feed(self, user_id):
        return stream_client.feed('user:%s' % user_id)

    def add_user_activity(self, user_id, activity):
        feed = stream_client.feed('user:%s' % user_id)
        result = feed.add_activity(activity)
        return result

    def remove_user_activity(self, user_id, activity):
        feed = stream_client.feed('user:%s' % user_id)
        result = feed.remove_activity(foreign_id=activity['foreign_id'])
        return result

    def _set_follow_user(self, user_id, target_id, method='follow'):
        '''
        Makes the aggregated:user_id and flat:user_id
        follow/unfollow
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

    def follow_user(self, follow):
        self._set_follow_user(
            follow.user_id, follow.target_id, method='follow')

    def unfollow_user(self, follow):
        return self._set_follow_user(follow.user_id, follow.target_id, method='unfollow')


manager = PinManager()
