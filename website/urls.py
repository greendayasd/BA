from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index', views.IndexView.as_view(), name='index'),
    path('history', views.HistoryView.as_view(), name='history'),
    path('ideas', views.IdeasView.as_view(), name='ideas'),
    path('createIdea', views.CreateIdeaView.as_view(), name='createIdea'),
    path('game', views.GameView.as_view(), name='game'),
    path('phasergame', views.PhaserGameView.as_view(), name='phasergame'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
