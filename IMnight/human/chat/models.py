from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from human.models import Relationship


class Message(models.Model):
    room = models.ForeignKey(
        Relationship, on_delete=models.CASCADE, related_name='messages')
    handle = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    # parse for json to send
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
