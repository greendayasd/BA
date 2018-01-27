from django.urls import path
from django.conf.urls import *
from . import views
from .views import IdeaViewSet, HistoryViewSet, OwnIdeasViewSet
from rest_framework import routers

app_name = 'website'

urlpatterns = [
    url(r'^$', views.homepage, name='index'),
    url(r'^$', HistoryViewSet.as_view, name='history'),
    url(r'^ideas/$', IdeaViewSet.as_view, name='idea-list'),
    url(r'^ideas/user/(?P<pk>\d+)/$', OwnIdeasViewSet.as_view, name='own-idea-list'),

    path('index', views.IndexView.as_view(), name='index'),
    path('history', views.HistoryView.as_view(), name='history'),
    path('ideas', views.IdeasView.as_view(), name='ideas'),
    url(r'^idea/new/$', views.idea_new, name='idea_new'),
    url(r'^idea/(?P<pk>\d+)/$', views.idea_detail, name='idea_detail'),
    path('phasergame', views.PhaserGameView.as_view(), name='phasergame'),

    # url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        views.activate, name='activate'),
]
