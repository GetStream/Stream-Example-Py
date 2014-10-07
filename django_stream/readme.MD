
###What this app does

This package makes it extremely easy to show a newsfeed to your user.
The screenshots clarify what we mean.

It's based on the open source Stream Framework and connects to the hosted getstream.io platform.

###Installation

pip install django_stream

add django_stream to your installed apps

python manage.py migrate

login with github at getstream.io and setup
STREAM_API_KEY and STREAM_API_SECRET

###Usage

Subclass Activity for activities you want to land in the feed

class Like(Activity):
    pass
    
class Comment(Activity):
    pass
    
class Pin(Activity):
	pass
    
The create and delete for these models will automatically hookup to the getstream.io API and
setup your newsfeeds.

###Custom activities


###Templating


