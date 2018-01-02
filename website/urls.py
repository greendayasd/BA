from django.urls import path, include
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
]