from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Idea, Version


class UserSerializer(serializers.HyperlinkedModelSerializer):
    ideas = serializers.HyperlinkedIdentityField('ideas', view_name='useridea-list', lookup_field='username')

    class Meta:
        model = User
        fields = ('id', 'username', 'ideas')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class IdeaSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(required=False)

    class Meta:
        model = Idea
        fields = '__all__'


class HistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Version
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts', )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    photos = serializers.HyperlinkedIdentityField('photos', view_name='postphoto-list')
    # author = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username')

    def get_validation_exclusions(self):
        # Need to exclude `author` since we'll add that later based off the request
        exclusions = super(PostSerializer, self).get_validation_exclusions()
        return exclusions + ['author']

    class Meta:
        model = Post
