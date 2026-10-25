from django import forms
from django.forms import inlineformset_factory

from .models import Household, Guest

class NameForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=60)
    surname = forms.CharField(label="Surname", max_length=60)

ReplyFormSet = inlineformset_factory(
    Household, 
    Guest, 
    fields=["reply_status"],
    extra=0,
    can_delete=False,
    )