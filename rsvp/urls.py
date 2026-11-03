from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("confirm/", views.confirm, name="confirm"),
    path("reply/", views.reply, name="reply"),
    path("thank-you/", views.thanks, name="thanks"),
    path("dietary/", views.dietary, name="dietary"),
    path("coach/", views.coach, name="coach"),
    path("accommodation/", views.accommodation, name="accommodation"),
    path("stay/", views.stay, name="stay"),
    path("extras/", views.extras, name="extras"),
]