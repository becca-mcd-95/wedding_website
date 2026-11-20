from django import forms
from django.forms import inlineformset_factory

from .models import Household, Guest

class NameForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=60)
    surname = forms.CharField(label="Surname", max_length=60)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ["reply_status"]
        widgets = {"reply_status": forms.RadioSelect(attrs={"class": "toggle"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reply_status"].choices = [
            (Guest.Status.YES, "Yes, I'll be there"),
            (Guest.Status.NO, "I can't make it"),
        ]

ReplyFormSet = inlineformset_factory(
    Household, 
    Guest, 
    fields=["reply_status"],
    form=ReplyForm,
    extra=0,
    can_delete=False,
    )

DietFormSet = inlineformset_factory(
    Household,
    Guest,
    fields=["diets", "dietary_notes"],
    widgets={"diets": forms.CheckboxSelectMultiple},
    extra=0,
    can_delete=False,
)

CoachFormSet = inlineformset_factory(
    Household,
    Guest,
    fields=["coach"],
    widgets={"coach": forms.RadioSelect},
    extra=0,
    can_delete=False,
)

AccommodationFormSet = inlineformset_factory(
    Household,
    Guest,
    fields=["needs_accommodation"],
    extra=0,
    can_delete=False,
)

class ExtrasForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ["comments", "email"]

class SitePasswordForm(forms.Form):
    password = forms.CharField(label="Password from your invite")
