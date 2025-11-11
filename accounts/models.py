from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import time


def default_reminder_time():
    """Default reminder time at 9:00 AM."""
    return time(9, 0)


class CustomUser(AbstractUser):
    """Custom user model with additional fields for MindCare."""
    
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Privacy and preferences
    allow_data_collection = models.BooleanField(default=True)
    allow_reminders = models.BooleanField(default=True)
    preferred_reminder_time = models.TimeField(default=default_reminder_time)
    
    # Profile information
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Account settings
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def age(self):
        """Calculate user's age from date of birth."""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class UserProfile(models.Model):
    """Extended profile information for users."""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Mental health preferences
    preferred_assessment_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
        ],
        default='weekly'
    )
    
    # Privacy settings
    public_profile = models.BooleanField(default=False)
    show_mood_trends = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"


class LoginAttempt(models.Model):
    """Track login attempts for security."""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{status} login attempt for {self.email} at {self.timestamp}"
