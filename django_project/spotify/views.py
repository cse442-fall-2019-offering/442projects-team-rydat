# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

songs = [
    {
        'title': 'Bad Day',
        'artist': 'Daniel Powter'
    },
    {
        'title': 'A Part of Me',
        'artist': 'Neck Deep'
    }
]

def main(request):
    return render(request, 'spotify/main.html', {'title': 'Main'}, )

def login(request):
    return render(request, 'spotify/login.html', {'title': 'Login'})

def generated(request):
    context = {
        'songs': songs
    }
    return render(request, 'spotify/generated.html', context)
