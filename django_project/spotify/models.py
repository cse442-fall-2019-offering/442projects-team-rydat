# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models

class Post(models.Model):
    playlist_name = models.CharField(max_length = 100)
    songs_from_playlist = models.TextField()
    date_generated = models.DateTimeField(default=timezone.now)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.playlist_name
