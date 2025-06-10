from django.contrib import admin
from .models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ['slug', 'original_url', 'user', 'clicks', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['slug', 'original_url']
    readonly_fields = ['slug', 'clicks', 'created_at']