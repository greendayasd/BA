from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'website'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index', views.IndexView.as_view(), name='index'),
    path('history', views.HistoryView.as_view(), name='history'),
    path('ideas', views.IdeasView.as_view(), name='ideas'),
    url(r'^idea/new/$', views.idea_new, name='idea_new'),
    url(r'^idea/(?P<pk>\d+)/$', views.idea_detail, name='idea_detail'),
    path('game', views.GameView.as_view(), name='game'),
    path('phasergame', views.PhaserGameView.as_view(), name='phasergame'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        views.activate, name='activate'),
]