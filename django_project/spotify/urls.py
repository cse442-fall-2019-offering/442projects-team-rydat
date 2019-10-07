from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='MooDuse-login'),
    url(r'^main/', views.main, name='MooDuse-main'),
    url(r'^playlist-generated/', views.generated, name='MooDuse-generated'),

]
