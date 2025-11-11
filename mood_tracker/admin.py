from django.contrib import admin
from .models import MoodEntry, MoodTrigger, MoodEntryTrigger

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood_rating', 'energy_level', 'anxiety_level', 'created_at']
    list_filter = ['mood_rating', 'energy_level', 'date', 'created_at']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(MoodTrigger)
class MoodTriggerAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_positive', 'description']
    list_filter = ['is_positive']
    search_fields = ['name', 'description']

@admin.register(MoodEntryTrigger)
class MoodEntryTriggerAdmin(admin.ModelAdmin):
    list_display = ['mood_entry', 'trigger', 'intensity']
    list_filter = ['trigger', 'intensity']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mood_entry__user', 'trigger')