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
    list_display = ['name', 'subscribers', 'is_deleted']
    list_filter = ['is_deleted']

    def get_queryset(self, request):
        return self.model.default.get_queryset()
