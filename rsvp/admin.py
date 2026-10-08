from django.contrib import admin
from .models import Household, Guest

class GuestAdmin(admin.ModelAdmin):
    list_display = ["first_name", "surname", "household", "reply_status"]

admin.site.register(Household)
admin.site.register(Guest, GuestAdmin)