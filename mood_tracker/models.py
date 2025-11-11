from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Okay'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]
    
    ENERGY_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'High'),
        (5, 'Very High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood_rating = models.IntegerField(choices=MOOD_CHOICES)
    energy_level = models.IntegerField(choices=ENERGY_CHOICES)
    anxiety_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rate from 1 (no anxiety) to 10 (severe anxiety)"
    )
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - Mood: {self.get_mood_rating_display()}"

class MoodTrigger(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_positive = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class MoodEntryTrigger(models.Model):
    mood_entry = models.ForeignKey(MoodEntry, on_delete=models.CASCADE, related_name='triggers')
    trigger = models.ForeignKey(MoodTrigger, on_delete=models.CASCADE)
    intensity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="How much did this trigger affect you? (1-5)"
    )
    
    class Meta:
        unique_together = ['mood_entry', 'trigger']