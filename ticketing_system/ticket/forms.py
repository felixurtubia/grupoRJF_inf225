from django import forms
from django.contrib.auth.models import User

from .models import Ticket, Keyword, TextData, FileData


class TicketForm(forms.ModelForm):
    asunto = forms.CharField(max_length=500, widget=forms.Textarea)
    contenido = forms.CharField(max_length=10000, widget=forms.Textarea)
    class Meta:
        model = Ticket
        fields = ['titulo', 'prioridad']


class KeywordForm(forms.ModelForm):

    class Meta:
        model = Keyword
        fields = ['nombre']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TextDataForm(forms.ModelForm):
    data_text = forms.CharField(max_length=1000, widget=forms.Textarea)

    class Meta:
        model = TextData
        fields = ['data_title']


class FileDataForm(forms.ModelForm):

    class Meta:
        model = FileData
        fields = ['data_title', 'data_file']