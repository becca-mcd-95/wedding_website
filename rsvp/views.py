from django.shortcuts import render, redirect, get_object_or_404
from .forms import NameForm
from .models import Guest

# Create your views here.

def index(request):
    matches = None
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            surname = form.cleaned_data["surname"]
            matches = Guest.objects.filter(first_name__iexact=first_name, surname__iexact=surname)
            if len(matches) == 1:
                request.session["guest_id"] = matches[0].id
                return redirect("confirm")
    else:
        form = NameForm()
    context = {"form": form, "matches": matches}
    return render(request, "rsvp/index.html", context)

def confirm(request):
    guest_id = request.session.get("guest_id")
    if guest_id is None:
        return redirect("index")
    guest = get_object_or_404(Guest, pk=guest_id)
    return render(request, "rsvp/confirm.html", {"guest": guest})

def reply(request):
    guest_id = request.session.get("guest_id")
    if guest_id is None:
        return redirect("index")
    guest = get_object_or_404(Guest, pk=guest_id)
    return render(request,"rsvp/reply.html", {"guest": guest})