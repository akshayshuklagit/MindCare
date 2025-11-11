from django.db import models
from django.conf import settings
from django.utils import timezone

class GratitudeEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.content[:50]}..."
