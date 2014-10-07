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
