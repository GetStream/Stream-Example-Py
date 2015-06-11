from stream_django import feed_manager


def user_feeds(request):
    context = {}
    if request.user.is_authenticated():
        for feed in ['user', 'flat', 'aggregated', 'notification']:
            context[feed + '_feed'] = feed_manager.get_feed(feed, request.user.id)
    return context


def unseen_notifications(request):
    context = {}
    if request.user.is_authenticated():
        feed = feed_manager.get_feed('notification', request.user.id)
        context['unseen_notifications'] = feed.get().get('unseen', 0)
        context['unread_notifications'] = feed.get().get('unread', 0)
    return context
