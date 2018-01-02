from .models import Idea, Version, User, Player
from .forms import IdeaForm
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


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


class GameView(generic.View):
    template_name = 'website/game.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/game.html')


class PhaserGameView(generic.View):
    template_name = 'website/phasergame.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/phasergame.html')


def idea_new(request):
    form = IdeaForm()
    return render(request, 'website/idea_form.html', {'form' : form})


def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        player = Player.objects.all().filter(user=request.user)[0]
        requests_left = player.requests_left
        if requests_left < 1:
            return render(request, 'website/ideas.html', {'vote': 'You already submited a request!'})

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            ver = Version.objects.all().order_by('-id')[0]
            post.version = ver
            post.save()
            player.requests_left -= 1
            player.save()

            return redirect('/website/ideas', pk=post.pk)
    else:
        form = IdeaForm()
    return render(request, 'website/idea_form.html', {'form': form})


class idea_detail(generic.DetailView):
    model = Idea
    template_name = 'website/idea.html'




