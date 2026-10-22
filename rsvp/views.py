from django.shortcuts import render
from .forms import NameForm

# Create your views here.

def index(request):
    searched_name = ""
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            surname = form.cleaned_data["surname"]
            searched_name = f"{first_name} {surname}"
    else:
        form = NameForm()
    context = {"form": form, "searched_name": searched_name}
    return render(request, "rsvp/index.html", context)