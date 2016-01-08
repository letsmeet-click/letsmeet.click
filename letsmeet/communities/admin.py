from django.contrib import admin
from django.db.models import Count

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
    list_display = ['name', 'show_subscriber_count', 'is_deleted']
    list_filter = ['is_deleted']

    def show_subscriber_count(self, obj):
        return obj.subscriber_count
    show_subscriber_count.admin_order_field = 'subscriber_count'
    show_subscriber_count.short_description = 'subscriber count'

    def get_queryset(self, request):
        return self.model.default.get_queryset().annotate(subscriber_count=Count('subscribers'))
