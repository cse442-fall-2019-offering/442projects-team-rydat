from django.shortcuts import render
from spotify.login_page import Login
from spotify.alanlogin import rob_login, rob_logout
import spotipy
from spotify.playlist_creator import Playlist_creator

userToken = None;
sp = None;

model = Playlist_creator()

def login(request):
    return render(request, 'spotify/login.html', {'title' : 'Login'})

def loginbutton(request):
    url = rob_login()
    context = {
        'title' : 'Approve this',
        'url' : url
    }
    return render(request, 'spotify/proceed.html', context)

def home(request):
    full_url = request.get_full_path()
    l = Login()
    global userToken
    userToken = None;
    userToken = l.getToken(full_url)
    global sp
    sp = spotipy.client.Spotify(auth=userToken['access_token'])
    context = {
        'title' : 'Home',
        'ouruser' : str(sp.current_user()['display_name']),
    }
    return render(request, 'spotify/home.html', context)

def generated(request):
    global userToken
    global sp
    text_to_eval = request.POST.get('feels')
    if text_to_eval is '':
        context = {
            'emotion': None,
            'token' : userToken,
            'ouruser' : str(sp.current_user()['display_name'])
        }
    else:
        resulting_id = model.create_playlist(text_to_eval, userToken)
        context = {
            'emotion': text_to_eval,
            'token': userToken,
            'playlist' : resulting_id,
            'ouruser' : str(sp.current_user()['display_name'])
        }
    return render(request, 'spotify/generated.html', context)

def logoutbutton(request):
    url = rob_logout()
    context = {
        'title' : 'Continue to log out',
        'url' : url
    }
    return render(request, 'spotify/logout.html', context)
