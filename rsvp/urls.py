from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("confirm/", views.confirm, name="confirm"),
    path("reply/", views.reply, name="reply"),
    path("thank-you/", views.thanks, name="thanks"),
    path("dietary/", views.dietary, name="dietary"),
]