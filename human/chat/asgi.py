import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMnight.im_settings")
channel_layer = channels.asgi.get_channel_layer()
