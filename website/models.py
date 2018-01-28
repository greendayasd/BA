from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import AbstractUser


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    requests_left = models.IntegerField(default=1)
    votes_left = models.IntegerField(default=1)
    email_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)
        instance.player.save()

    def player_set_requests(self, new_requests):
        self.requests_left = new_requests

    def player_increase_requests(self):
        self.requests_left += 1

    def player_decrease_requests(self):
        self.requests_left -= 1

    def __str__(self):
        return self.user.username

    def current_version_beaten (self):
        ver = Version.objects.all().order_by('-id')[0]
        current = GameInfo.objects.all().filter(version=ver,user=self.user)
        return current.rounds_won >= 1


class Version(models.Model):
    label = models.CharField(max_length=20,unique=True)
    change = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    submitter = models.ForeignKey(Player, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.label

    def is_newest(self):
        if self == Version.objects.latest():
            return True
        return False


class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name='ideas')
    request_text = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    estimated_time = models.CharField(max_length=50, null=True, default='')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    #
    # votes = models.IntegerField(default=0)
    #

    def __str__(self):
        return self.request_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_newest_version(self):
        ver = Version.objects.all().order_by('-id')[0]
        return self.version == ver


class GameInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gameinfo')
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name='gameinfo')
    rounds_won = models.IntegerField(default=0)
    rounds_lost = models.IntegerField(default=0)
    enemies_killed = models.IntegerField(default=0)
    coins_collected = models.IntegerField(default=0)
    highscore = models.IntegerField(default=-1)

    def __str__(self):
        return self.version.label + '  ' + self.user.username + '  ' + self.rounds_won + ...
        '/' + (self.rounds_won + self.rounds_lost)


class WebsiteInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='websiteinfo')
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True, related_name='websiteinfo')
    time_spent_game = models.IntegerField(default=0)
    time_spent_ideas = models.IntegerField(default=0)
    time_spent_index = models.IntegerField(default=0)
    time_spent_history = models.IntegerField(default=0)
    time_spent_chat = models.IntegerField(default=0)

