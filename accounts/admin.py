from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, UserProfile, LoginAttempt


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    
    fieldsets = (
        ('Avatar', {
            'fields': ('avatar',)
        }),
        ('Mental Health Preferences', {
            'fields': ('preferred_assessment_frequency',)
        }),
        ('Privacy Settings', {
            'fields': ('public_profile', 'show_mood_trends')
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom user admin with additional fields."""
    
    # Fields to display in the user list
    list_display = [
        'email', 'username', 'first_name', 'last_name', 
        'is_active', 'email_verified', 'date_joined', 'last_login'
    ]
    
    # Fields to filter by
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'email_verified', 
        'allow_data_collection', 'allow_reminders', 'date_joined'
    ]
    
    # Fields to search
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    # Default ordering
    ordering = ['-date_joined']
    
    # Add the profile inline
    inlines = [UserProfileInline]
    
    # Custom fieldsets for the user detail/edit page
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'location')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Privacy & Preferences', {
            'fields': (
                'allow_data_collection', 'allow_reminders', 
                'preferred_reminder_time', 'timezone'
            )
        }),
        ('Profile Information', {
            'fields': ('bio',)
        }),
        ('Account Status', {
            'fields': ('is_active', 'email_verified')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name')
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_email', 'preferred_assessment_frequency', 
        'public_profile', 'show_mood_trends', 'created_at'
    ]
    list_filter = [
        'preferred_assessment_frequency', 'public_profile', 
        'show_mood_trends', 'created_at'
    ]
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar')
        }),
        ('Mental Health Preferences', {
            'fields': ('preferred_assessment_frequency',)
        }),
        ('Privacy Settings', {
            'fields': ('public_profile', 'show_mood_trends')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'success_status', 'ip_address', 
        'user_agent_short', 'timestamp'
    ]
    list_filter = ['success', 'timestamp']
    search_fields = ['email', 'ip_address', 'user_agent']
    readonly_fields = [
        'user', 'email', 'ip_address', 'user_agent', 
        'success', 'timestamp'
    ]
    
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Login Information', {
            'fields': ('user', 'email', 'success')
        }),
        ('Session Details', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    def success_status(self, obj):
        if obj.success:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Success</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Failed</span>'
            )
    success_status.short_description = 'Status'
    success_status.admin_order_field = 'success'
    
    def user_agent_short(self, obj):
        return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
    user_agent_short.short_description = 'User Agent'
    
    def has_add_permission(self, request):
        return False  # Login attempts are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Login attempts should not be modified
