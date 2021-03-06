from .models import Idea, Version, Player
from .forms import IdeaForm, SignUpForm
from .tokens import account_activation_token
from django.shortcuts import render, redirect, render_to_response
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, IdeaSerializer, HistorySerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all() #.order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    # ver = Version.objects.all().order_by('-pub_date')[0]
    # queryset = Idea.objects.all().filter(version=ver).order_by('-pub_date')
    queryset = Idea.objects.all()
    lookup_field = 'id'
    serializer_class = IdeaSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user


class OwnIdeasViewSet(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer

    def get_queryset(self):
        return Idea.objects.filter(self.request.user)


class IdeasViewSet(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer

    def get_queryset(self):
        ver = Version.objects.all().order_by('-id')[0]
        return Idea.objects.filter(version=ver)


class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySerializer

    def get_queryset(self):
        return Version.objects.all()


def homepage(request):
    return render(request, 'website/home.html')

# class IndexTestView(generic.View):
#     template_name = 'website/indextest.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, 'website/home.html')




# old views
class IndexView(generic.View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits+1
        version = Version.objects.all().order_by('-id')[0]
        versionLabel = version.label

        return render(request, 'website/index.html', context={
            'num_visits':num_visits, 'version':versionLabel}, # num_visits appended

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
        ver = Version.objects.all().order_by('-pub_date')[0]
        return Idea.objects.filter(version=ver).order_by('-pub_date')


class GameView(generic.View):
    template_name = 'website/game.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/game_alt.html')


class PhaserGameView(generic.View):
    template_name = 'website/phasergame.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/phasergame.html')


# @login_required()
# def idea_new(request):
#     form = IdeaForm()
#     return render(request, 'website/idea_form.html', {'form' : form})


@login_required()
def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST)
        player = Player.objects.all().filter(user=request.user)[0]
        requests_left = player.requests_left
        if requests_left < 1:
            #return redirect('/website/ideas', {'vote': 'You already submited a request!'})
            return render(request, 'website/ideas.html', {'vote': 'You already '
                                                                      'submited a request this cycle!'})
        elif form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            ver = Version.objects.all().order_by('-id')[0]
            post.version = ver
            post.save()
            player.requests_left -= 1
            player.save()

            return redirect('ideas', pk=post.pk)
    else:
        form = IdeaForm()
    return render(request, 'website/idea_form.html', {'form': form})


class idea_detail(generic.DetailView):
    model = Idea
    template_name = 'website/idea.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
            except Player.DoesNotExist:
                user = Player(user=request.user)
            # user.refresh_from_db()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Crowdjump Account'
            newuid = force_text(urlsafe_base64_encode(force_bytes(user.pk)))
            message = render_to_string('website/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'uid': newuid,
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('website:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'website/signup.html', {'form': form}, RequestContext(request))


def account_activation_sent(request):
    return render(request, 'website/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Player.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.player.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('website:index')
    else:
        return render(request, 'website/account_activation_invalid.html')

