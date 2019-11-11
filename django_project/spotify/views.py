from django.shortcuts import render
from django.http import HttpResponse
from spotify.login_page import Login
import spotipy
from spotify.playlist_creator import dakota_creation
from spotify.playlist import Mooduseplaylists

userToken = None;
sp = None;

def login(request):
    return render(request, 'spotify/login.html', {'title': 'Login'})

def home(request):
    full_url = request.get_full_path()
    l = Login()
    global userToken
    userToken = l.getToken(full_url)
    global sp
    sp = spotipy.client.Spotify(auth=userToken['access_token'])

    context = {
        'title' : 'Home',
        'ouruser' : str(sp.current_user()['display_name']),
        'oldPlaylists': Mooduseplaylists(userToken['access_token'])
    }

    return render(request, 'spotify/home.html', context)

def loginbutton(request):
      l = Login()
      l.login()
      context =  {
        'func' : l,
        'title' : 'Close this',
        }
      return render(request,'spotify/close.html' , context)  # dynamic call

def logoutbutton(request):
    l = Login()
    l.logout()
    context = {
        'func' : l,
        'title' : 'Logged Out',
    }
    return render(request, 'spotify/logout.html', context)

def generated(request):
    global userToken
    global sp
    input = request.POST.get('feels')
    if input is '':
        context = {
            'emotion': None,
            'token' : userToken,
            'ouruser' : str(sp.current_user()['display_name'])
        }
    else:
        resulting_id = dakota_creation(input, userToken)
        context = {
            'emotion': input,
            'token': userToken,
            'playlist' : resulting_id,
            'ouruser' : str(sp.current_user()['display_name'])

            }
    return render(request, 'spotify/generated.html', context)
