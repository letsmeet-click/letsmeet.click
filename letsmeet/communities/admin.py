from django.contrib import admin

from .models import (
    Community,
)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    pass
