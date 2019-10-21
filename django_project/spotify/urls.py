from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='mooduse-login'), # our login is created in views.py where login is defined
    path('home/', views.home, name='mooduse-home'),
    path('close/', views.loginbutton,name='login-button'),
    path('playlist-generated/', views.generated, name='mooduse-generated'),
    path('logged-out/', views.logoutbutton, name='logout-button'),
    path('again/', views.login, name='newplaylist-button'),
]
