from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models

class Post(models.Model):
    playlist_name = models.CharField(max_length = 100)
    # songs_from_playlist = models.TextField()                        #user input
    date_generated = models.DateTimeField(default=timezone.now)
    # requester = models.ForeignKey(User, on_delete=models.CASCADE)  #if you delete this field from db then all the references will be removed aswell

    def __str__(self):
        return self.playlist_name



#https://docs.djangoproject.com/en/2.2/topics/db/models/

#https://docs.djangoproject.com/en/2.2/topics/db/queries/