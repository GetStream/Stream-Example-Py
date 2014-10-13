
from stream_django import feed_manager

def user_feeds(request):
    context = {}
    if request.user.is_authenticated():
        for feed in ['user', 'flat', 'aggregated', 'notification']:
            context[feed] = feed_manager.get_feed(request.user.id, feed)
        
    return context
    