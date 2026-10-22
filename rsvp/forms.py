from django import forms

class NameForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=60)
    surname = forms.CharField(label="Surname", max_length=60)