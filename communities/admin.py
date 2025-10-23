from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Community, Sponsor, Sponsorship, Event


@admin.register(Community)
class CommunityAdmin(ModelAdmin):
    list_display = ("name", "location", "verified", "sponsors_count", "funded_recently", "last_active")
    list_filter = ("verified", "funded_recently", "location")
    search_fields = ("name", "description", "location")


@admin.register(Sponsor)
class SponsorAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Sponsorship)
class SponsorshipAdmin(ModelAdmin):
    list_display = ("community", "sponsor", "amount", "contribution_type", "date")
    list_filter = ("contribution_type", "date")
    search_fields = ("community__name", "sponsor__name")


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("community", "title", "date")
    list_filter = ("date",)
    search_fields = ("title", "community__name")
