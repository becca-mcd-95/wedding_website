from django.shortcuts import render, redirect, get_object_or_404
from .forms import NameForm, ReplyFormSet, DietFormSet, CoachFormSet, AccommodationFormSet, ExtrasForm
from .models import Guest

# Create your views here.

def get_session_guest(request):
    guest_id = request.session.get("guest_id")
    if guest_id is None:
        return None
    return get_object_or_404(Guest, pk=guest_id)

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
    guest = get_session_guest(request)
    if guest is None:
        return redirect("index")
    return render(request, "rsvp/confirm.html", {"guest": guest})

def reply(request):
    guest = get_session_guest(request)
    if guest is None:
        return redirect("index")
    if request.method == "POST":
        formset = ReplyFormSet(request.POST, instance=guest.household)
        if formset.is_valid():
            formset.save()
            attending = guest.household.guests.filter(reply_status=Guest.Status.YES)
            if attending.exists():
                return redirect("dietary")
            return redirect("thanks")
    else:
        formset = ReplyFormSet(instance=guest.household)
    return render(request,"rsvp/reply.html", {"guest": guest, "formset": formset})

def thanks(request):
    return render(request, "rsvp/thanks.html")

def dietary(request):
    guest = get_session_guest(request)
    if guest is None:
        return redirect("index")
    attending = guest.household.guests.filter(reply_status=Guest.Status.YES)
    if request.method == "POST":
        formset = DietFormSet(request.POST, queryset=attending, instance=guest.household)
        if formset.is_valid():
            formset.save()
            return redirect("accommodation")
    else:
        formset = DietFormSet(queryset=attending, instance=guest.household)
    return render(request, "rsvp/dietary.html", {"guest": guest, "formset": formset})

def coach(request):
    guest = get_session_guest(request)
    if guest is None:
        return redirect("index")
    attending = guest.household.guests.filter(reply_status=Guest.Status.YES)
    if request.method == "POST":
        formset = CoachFormSet(request.POST, queryset=attending, instance=guest.household)
        if formset.is_valid():
            formset.save()
            return redirect("extras")
    else: 
        formset = CoachFormSet(queryset=attending, instance=guest.household)
    return render(request, "rsvp/coach.html", {"guest": guest, "formset": formset})

def accommodation(request):
    guest = get_session_guest(request)
    if guest is None:
        return redirect("index")
    attending = guest.household.guests.filter(reply_status=Guest.Status.YES)
    if request.method == "POST":
        formset = AccommodationFormSet(request.POST, queryset=attending, instance=guest.household)
        if formset.is_valid():
            formset.save()
            needs_stay = attending.filter(needs_accommodation=True)
            if needs_stay.exists():
                return redirect("stay")
            return redirect("coach")
    else: 
        formset = AccommodationFormSet(queryset=attending, instance=guest.household)
    return render(request, "rsvp/accommodation.html", {"guest": guest, "formset": formset})

def stay(request):
    return render(request, "rsvp/stay.html")

def extras(request):
    guest = get_session_guest(request)
    if guest is None:
        return redirect("index")
    if request.method == "POST":
        form = ExtrasForm(request.POST, instance=guest.household)
        if form.is_valid():
            form.save()
            return redirect("thanks")
    else: 
        form = ExtrasForm(instance=guest.household)
    return render(request, "rsvp/extras.html", {"guest": guest, "form": form})