## Stream Example App

This example Django app shows you how you can use [GetStream.io](https://getstream.io/ "GetStream.io") to built a site similar to Pinterest.

### Demo

You can [try the demo here](http://exampledjango.getstream.io).
Alternatively you can deploy your own copy of the demo via Heroku.

### Heroku

The best way to try this application is via Heroku; you can deploy this example (for free) on Heroku
by pressing the Deploy button below.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

If you prefer to run this locally then make sure to follow the steps in the install file.


## Tutorial

So we want the pins, comments and follows to show up in the user's feed. We start by installing stream_django

```pip install stream_django```

add stream_django to your ```INSTALLED_APPS```

```
INSTALLED_APPS = [
    ...
    'stream_django'
]
```

We indicate which models should be shared by using the Activity mixin.

```
class Pin(Activity, models.Model):
    ...
```
    
Now when users will add a pin it will automatically show up on the user feed. However to setup the newsfeed we also need
to know who follows who. 

```
feed_manager.follow_user(user_id, target_id)
```

This is all that's needed to setup the newsfeed. To retrieve the newsfeed we use the following code

```
@login_required
def feed(request):
    '''
    Items pinned by the people you follow
    '''
    enricher = Enrich(request.user)
    context = RequestContext(request)
    feed = feed_manager.get_news_feeds(request.user.id)['flat']
    if request.REQUEST.get('delete'):
        feed.delete()
    activities = feed.get(limit=25)['results']
    context['activities'] = enricher.enrich_activities(activities)
    response = render_to_response('core/feed.html', context)
    return response
```

The last bit of work is making sure the templates render nicely.

```
{% for activity in activities %}
    {% render_activity activity %}
{% endfor %}
```

This will render the templates in

https://github.com/GetStream/Stream-Example-Py/tree/master/templates/activity
