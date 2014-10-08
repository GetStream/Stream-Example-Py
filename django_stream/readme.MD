
###Stream_django

This package helps you integrate your Django projects with GetStream.io


###Features
Settings integration for client keys  
Model integration  
Activity template helpers  
Notification feed integration  

###Installation

Install django_stream package with pip:

```pip install django_stream```

add django_stream to your ```INSTALLED_APPS```

```
INSTALLED_APPS = [
    ...
    'django_stream'
]
```

Login to getstream.io and add
```STREAM_API_KEY``` and ```STREAM_API_SECRET``` to your Django settings module (you can find them in the dashboard).

###Model integration

You can have django_stream take care automatically of adding/removing model instances to user feeds; to do that let the model classes that need to be stored in feeds inherit from ```django_stream.activity.Activity```

```
class Tweet(models.Model, Activity):
    ...
```

From now on every time a Tweet is created; an activity referencing it will be added to its user' feed; feeds that follow that user will also automatically get the new tweet automatically in their feeds.

####Activity fields

Models are stored in feeds as activities; an activity is composed by the following fields: **actor**, **verb**, **object** and by other optional extra fields.  
The Activity class comes with a built-in capability of present an instance as an activity.

**object** is a reference to the model instance  
**actor** is a reference to the user attribute of the instance  
**verb** is a nice string representation of the class name

While you probably won't need to change the object field; you will probably need to adjust the other two fields to fit with your data.

```
class Tweet(models.Model, Activity):
    author = models.ForeignKey('core.User')

    @property
    def verb(self):
        return 'shout'

    @property
    def actor_attr(self):
        return self.author

```


The create and delete for these models will automatically hookup to the getstream.io API and
setup your newsfeeds.

###Custom activities


###Templating


