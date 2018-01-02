from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    highscore = models.IntegerField(default=-1)
    requests_left = models.IntegerField(default=1)
    rounds_played = models.IntegerField(default=0)
    current_version_beaten = models.BooleanField(default=False)
    votes_left = models.IntegerField(default=1)


    @receiver(post_save, sender=User)
    def create_player(sender, instance, created, **kwargs):
        if created:
            Player.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_player(sender, instance, **kwargs):
        instance.player.save()

    def player_increase_rounds(self):
        self.rounds_played +=1

    def player_set_highscore(self, new_highscore):
        if new_highscore < self.highscore:
            self.highscore = new_highscore

    def player_increase_time_played(self, playtime):
        self.time_played += playtime

    def player_set_requests(self, new_requests):
        self.requests_left = new_requests

    def player_increase_requests(self):
        self.requests_left += 1

    def player_decrease_requests(self):
        self.requests_left -= 1

    def __str__(self):
        return self.user.username


class Version(models.Model):
    label = models.CharField(max_length=20,unique=True)
    change = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    submitter = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.label

    def is_newest(self):
        if self == Version.objects.latest():
            return True
        return False


class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_text = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published', default=datetime.now)
    version = models.ForeignKey(Version, on_delete=models.CASCADE, null=True)
    #
    # votes = models.IntegerField(default=0)
    #

    def __str__(self):
        return self.request_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_newest_version(self):
        return self.version == self.version


