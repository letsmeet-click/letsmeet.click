from django.contrib import admin

from .models import (
    Community, CommunitySubscription,
)


class CommunitySubscriptionInline(admin.TabularInline):
    model = CommunitySubscription
    extra = 1


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    inlines = [
        CommunitySubscriptionInline,
    ]
