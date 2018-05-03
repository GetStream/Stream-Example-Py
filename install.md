1. create and activate a virtual environment
2. install requirements with `pip install -r requirements.txt`
3. create an account on https://getstream.io
4. Use the default created app or create a new one with the feeds with the
   following names and types:

    a. user, flat
    b. notification, notification
    c. timline, flat
    d. timline_aggregated, aggregated

5. get your API credentials (key and secret) and add them to the bottom of
   `core/settings.py` (STREAM_API_KEY and STREAM_API_SECRET)
6. Change the following settings in `core/settings.py`:

```python
DEBUG = True

...

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdatabase.sqlite',
    }
}

```

7. install ruby dependencies (compass) via bundler `bundler` or with gem `gem install compass`
8. initialize your app `python manage.py after_deploy`
9. collect static files `python manage.py collectstatic`
10. compress the static files `python manage.py compress`
11. start the webserver `python manage.py runserver`
12. open your browser on http://localhost:8000

If you have any problems please open a issue on github and paste any error you get in the console.
