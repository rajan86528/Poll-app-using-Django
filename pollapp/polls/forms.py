from django import forms
from django.contrib.auth.models import User


from .models import Poll, Choice

from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        

    def save(self, commit=True):
        poll = super().save(commit=commit)
        return poll