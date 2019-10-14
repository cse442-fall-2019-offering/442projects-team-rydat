# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

sad_songs = [
    {
        'title': 'Bad Day',
        'artist': 'Daniel Powter',
        'type': 'sad'
    },
    {
        'title': 'A Part of Me',
        'artist': 'Neck Deep',
        'type': 'sad'
    }
]

happy_songs = [
    {
        'title': 'Satellite',
        'artist': 'Cash Cash',
        'type': 'happy'
    },
    {
        'title': 'Uptown Funk',
        'artist': 'Bruno Mars',
        'type': 'happy'
    }
]

angry_songs = [
    {
        'title': 'Disturbed',
        'artist': 'Down With The Sickness',
        'type': 'angry'
    },
    {
        'title': 'Papa Roach',
        'artist': 'Last Resort',
        'type': 'angry'
    }
]


def main(request):
    return render(request, 'spotify/main.html', {'title': 'Main'}, )

def login(request):
    return render(request, 'spotify/login.html', {'title': 'Login'})

def generated(request):
    input = request.POST.get('feels')

    if(input == 'sad'):
        context = {
            'songs': sad_songs,
            'playlist': 'sad'
        }
    elif(input == 'happy'):
        context = {
            'songs': happy_songs,
            'playlist': 'happy'
        }
    elif(input == 'angry'):
        context = {
            'songs': angry_songs,
            'playlist': 'angry'
        }
    else:
        context = {

        }

    return render(request, 'spotify/generated.html', context)
