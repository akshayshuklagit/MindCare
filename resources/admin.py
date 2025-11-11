from django.contrib import admin
from .models import ResourceCategory, Resource, CrisisResource


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'resource_type', 'difficulty_level', 'view_count', 'is_featured', 'is_active']
    list_filter = ['category', 'resource_type', 'difficulty_level', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'summary', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'resource_type')
        }),
        ('Content', {
            'fields': ('summary', 'content', 'external_url')
        }),
        ('Metadata', {
            'fields': ('difficulty_level', 'estimated_read_time', 'tags')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )





@admin.register(CrisisResource)
class CrisisResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'country', 'is_crisis_line', 'priority', 'is_active']
    list_filter = ['country', 'is_crisis_line', 'is_text_support', 'is_chat_support', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['priority', 'name']


