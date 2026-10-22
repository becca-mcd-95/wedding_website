from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("rsvp/", include("rsvp.urls")),
    path('admin/', admin.site.urls),
]
