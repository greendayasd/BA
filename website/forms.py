from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Idea, Player


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Enter a unique email address')

    class Meta:
        model = User
        help_texts = {
            'username': '',
        }
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and can not be entirely numeric'
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class IdeaForm(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ('request_text', 'description',)


