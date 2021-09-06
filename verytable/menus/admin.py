from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Menu, Reservation, SiteProperty


class MenuAdmin(SummernoteModelAdmin):
    model = Menu
    list_display = ["date", "title", "price"]
    list_filter = ["date"]
    summernote_fields = ('presentation',)


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ["name", "menu", "pax"]
    list_filter = ["menu"]

class SitePropertyAdmin(admin.ModelAdmin):
    model = SiteProperty


admin.site.register(Menu, MenuAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(SiteProperty, SitePropertyAdmin)
