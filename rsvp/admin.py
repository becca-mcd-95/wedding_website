from django.contrib import admin
from .models import Household, Guest

class GuestInLine(admin.TabularInline):
    model = Guest
    extra = 3

class GuestAdmin(admin.ModelAdmin):
    list_display = ["first_name", "surname", "household", "reply_status"]

class HouseHoldAdmin(admin.ModelAdmin):
    list_display = ["name", "invite_type"]
    inlines = [GuestInLine]


admin.site.register(Household, HouseHoldAdmin)
admin.site.register(Guest, GuestAdmin)