from django.shortcuts import render          
from django.http import HttpResponse
from spotify.login_page import Login




#when user enters main page ... check if there is token ... to see if they are logged in
#if they are : then we have access to their spotipy obj
# if not , redirect them to Login.html so they can Connect

def home(request):

      return render(request,'spotify/index.html' ) 



def login(request):     
      return render(request,'spotify/login.html') 



def button(request): 
      l = Login()
      l.__init__
      l.login()
      context =  {
            'func' : l  
            } 
      # token = l.getToken(l.REDIRECT_URI)
      return render(request,'spotify/login.html' , context)  # dynamic call 



