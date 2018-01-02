from .models import Idea, Version
from django.shortcuts import render
from django.views import generic


class IndexView(generic.View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits+1
        return render(request, 'website/index.html', context={
            'num_visits':num_visits}, # num_visits appended

    )


class HistoryView(generic.ListView):
    model = Version
    template_name = 'website/history.html'

    def get_queryset(self):
        return Version.objects.all().order_by('-pub_date')


class IdeasView(generic.ListView):
    template_name = 'website/ideas.html'
    model = Idea
    context_object_name = 'idea_list'

    def get_queryset(self):
        return Idea.objects.order_by('-pub_date')


class CreateIdeaView(generic.View):
    template_name = 'website/createIdea.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/createIdea.html')


class GameView(generic.View):
    template_name = 'website/game.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/game.html')


class PhaserGameView(generic.View):
    template_name = 'website/phasergame.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/phasergame.html')

