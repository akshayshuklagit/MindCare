from django.contrib import admin
from .models import GratitudeEntry

@admin.register(GratitudeEntry)
class GratitudeEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'content_preview', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
