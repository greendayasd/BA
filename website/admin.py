from django.contrib import admin

from .models import Question, Idea, Choice, Version, Player
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.admin.helpers import ActionForm
from django import forms

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        (None, {'fields': ['request_text']}),
        (None, {'fields': ['description']}),
        (None, {'fields': ['version']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('user', 'request_text', 'pub_date', 'version', 'is_newest_version')
    list_filter = ['pub_date', 'version']
    search_fields = ['request_text', 'version']


def admin_mail(modeladmin, request, queryset):
    version = Version.objects.all().order_by('-id')[0]
    subject = request.POST['subject']
    if subject == '' or subject == 'a':
        subject = 'New Crowdjump version is online!'

    message = request.POST['message']
    if message == '' or message == 'a':
        message = 'Version ' + version.label + ' of Crowdjump is available now! \n ' \
                                         'Test it at https://crowdjump.win/website/phasergame'

    receivers = []
    for obj in queryset:
        receivers.append(obj.user.email)
    # for user in User.objects.all():
    #     receivers.append(user.email)

    send_mail(subject, message, 'crowdjump@gmail.com', receivers)


class MailForm(ActionForm):

    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=100)


class MailAdmin(admin.ModelAdmin):
    action_form = MailForm
    actions = [admin_mail]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Version)
admin.site.register(Player,MailAdmin)
admin.site.register(Idea, IdeaAdmin)
