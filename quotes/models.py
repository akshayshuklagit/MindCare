from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Quote(models.Model):
    CATEGORY_CHOICES = [
        ('motivation', 'Motivation'),
        ('mindfulness', 'Mindfulness'),
        ('anxiety', 'Anxiety'),
        ('depression', 'Depression'),
        ('self_care', 'Self Care'),
        ('positivity', 'Positivity'),
        ('resilience', 'Resilience'),
    ]
    
    text = models.TextField()
    author = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='motivation')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.text[:50]}..."

class UserFavoriteQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'quote']
    
    def __str__(self):
        return f"{self.user.username} - {self.quote.text[:30]}..."

class DailyQuote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Daily quote for {self.date}"