from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Question, Idea, Choice, Version
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone


class IndexView(View):
    template_name = 'website/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'website/index.html')


class HistoryView(generic.ListView):
    model = Version
    template_name = 'website/history.html'

    def get_queryset(self):
        return Version.objects.all().order_by('pk')


class IdeasView(generic.ListView):
    template_name = 'website/ideas.html'
    context_object_name = 'latest_idea_list'

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


def logout_view(request):
    logout(request)
    # Redirect to a success page.


def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...


def player_increase_rounds(request, user_id):
    user = User.objects.get(pk=user_id)
    user.player.rounds_played += 1
    user.save()


def player_set_highscore(request, user_id, new_highscore):
    user = User.objects.get(pk=user_id)
    if new_highscore < user.player.highscore:
        user.player.highscore = new_highscore
    user.save()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please activate your CrowdJump Account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your activation e-mail! ')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation.')
    else:
        return HttpResponse('The activation link is invalid!')