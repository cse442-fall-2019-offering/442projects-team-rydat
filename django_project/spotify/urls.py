from django.urls import path
from . import views

urlpatterns = [
        path('', views.login, name='mooduse-login'),
        path('proceed/', views.loginbutton, name='login-button'),
        path('home/', views.home, name='mooduse-home'),
        path('playlist-generated/', views.generated, name='mooduse-generated'),
        path('logged-out/', views.logoutbutton, name='logout-button'),
        path('again/', views.login, name='newplaylist-button'),
]
