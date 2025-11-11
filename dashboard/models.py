from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserGoal(models.Model):
    GOAL_TYPES = [
        ('mood', 'Mood Improvement'),
        ('anxiety', 'Anxiety Management'),
        ('sleep', 'Better Sleep'),
        ('exercise', 'Regular Exercise'),
        ('mindfulness', 'Mindfulness Practice'),
        ('social', 'Social Connection'),
        ('custom', 'Custom Goal'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_value = models.IntegerField(help_text="Target number (days, sessions, etc.)")
    current_progress = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(default=timezone.now)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def progress_percentage(self):
        if self.target_value > 0:
            return min(100, (self.current_progress / self.target_value) * 100)
        return 0
    
    @property
    def is_completed(self):
        return self.current_progress >= self.target_value

class DashboardWidget(models.Model):
    WIDGET_TYPES = [
        ('mood_chart', 'Mood Chart'),
        ('quote_of_day', 'Quote of the Day'),
        ('goals_progress', 'Goals Progress'),
        ('recent_assessments', 'Recent Assessments'),
        ('mood_streak', 'Mood Tracking Streak'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPES)
    position = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    settings = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ['user', 'widget_type']
        ordering = ['position']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_widget_type_display()}"