from django.contrib import admin
from .models import UserGoal, DashboardWidget

@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'goal_type', 'progress_display', 'status', 'target_date']
    list_filter = ['goal_type', 'status', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    date_hierarchy = 'created_at'
    
    def progress_display(self, obj):
        return f"{obj.current_progress}/{obj.target_value} ({obj.progress_percentage:.1f}%)"
    progress_display.short_description = 'Progress'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'widget_type', 'position', 'is_visible']
    list_filter = ['widget_type', 'is_visible']
    search_fields = ['user__username']
    list_editable = ['position', 'is_visible']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')