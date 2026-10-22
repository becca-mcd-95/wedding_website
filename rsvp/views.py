from django.shortcuts import render
from django.http import HttpResponse

from .forms import NameForm

# Create your views here.

def index(request):
    form = NameForm()
    context = {"form": form}
    return render(request, "rsvp/index.html", context)