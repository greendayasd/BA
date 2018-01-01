from django.contrib import admin

from .models import Question, Idea, Choice, Version, Player
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
        (None, {'fields': ['player']}),
        (None, {'fields': ['request_text']}),
        (None, {'fields': ['description']}),
        (None, {'fields': ['version']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('player', 'request_text', 'pub_date', 'version', 'is_newest_version')
    list_filter = ['pub_date', 'version']
    search_fields = ['request_text', 'version']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Version)
admin.site.register(Player)
admin.site.register(Idea, IdeaAdmin)
