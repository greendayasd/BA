from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Idea, Version


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class IdeaSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Idea
        fields = '__all__'


class HistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Version
        fields = '__all__'
