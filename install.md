1. create and activate a virtual environment
2. install requirements with `pip install -r requirements.txt`
3. create an account on https://getstream.io
4. Use the default created app or create a new one with the feeds with the
   following names and types:

    a. user, flat
    b. notification, notification
    c. timline, flat
    d. timline_aggregated, aggregated

5. get your API credentials (key and secret) and store them in settings.py (STREAM_API_KEY and STREAM_API_SECRET)
6. install ruby dependencies (compass) via bundler `bundler` or with gem `gem install compass`
7. initialize your app `python manage.py after_deploy`
8. collect static files `python manage.py collectstatic`
9. start the webserver `python manage.py runserver`
10. open your browser on http://localhost:8000

If you have any problems please open a issue on github and paste any error you get in the console.
