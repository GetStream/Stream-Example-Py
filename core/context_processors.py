
from stream_django import feed_manager

def user_feeds(request):
    context = {}
    if request.user.is_authenticated():
        for feed in ['user', 'flat', 'aggregated', 'notification']:
            context[feed + '_feed'] = feed_manager.get_feed(feed, request.user.id)
        
    return context
    