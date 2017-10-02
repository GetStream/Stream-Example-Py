## Stream Django Example App

This example Django app shows you how you can easily build a site similar to Pinterest.

The project is based on the [stream-django](https://github.com/GetStream/stream-django) integration for [Stream](https://getstream.io/). There is also a lower level [Python - Stream integration](https://github.com/getstream/stream-python) library which is suitable for all Python applications.

You can sign up for a Stream account at https://getstream.io/get_started.

If you're looking to self-host your feed solution we suggest the open source [Stream-Framework](https://github.com/tschellenbach/Stream-Framework), created by the Stream founders.

### Live demo

Try the [live demo](http://exampledjango.getstream.io).

## Deploying the app

### Heroku

The best way to understand and try out this application is via Heroku. You can deploy the app, for free, simply by clicking the following button:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

### Local

If you prefer to run the project locally, simply follow the steps in the [install.md](install.md) file.

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
    feed = feed_manager.get_news_feeds(request.user.id)['timeline']
    if request.POST.get('delete'):
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

## Copyright and License Information

Copyright (c) 2014-2017 Stream.io Inc, and individual contributors. All rights reserved.

See the file "LICENSE" for information on the history of this software, terms & conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.
