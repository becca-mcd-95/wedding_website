from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("guest/<int:guest_id>/", views.confirm, name="confirm"),
]