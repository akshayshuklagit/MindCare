from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import uuid

User = get_user_model()


class AssessmentType(models.Model):
    """Different types of mental health assessments."""
    
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=10)  # PHQ9, GAD7, etc.
    description = models.TextField()
    instruction = models.TextField(help_text="Instructions shown to users before taking the assessment")
    
    # Scoring configuration
    max_score = models.PositiveIntegerField()
    scoring_method = models.CharField(
        max_length=20,
        choices=[
            ('sum', 'Sum of all answers'),
            ('average', 'Average of all answers'),
            ('weighted', 'Weighted scoring'),
        ],
        default='sum'
    )
    
    # Display settings
    is_active = models.BooleanField(default=True)
    requires_login = models.BooleanField(default=False)
    estimated_time = models.PositiveIntegerField(help_text="Estimated time in minutes")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.short_name})"
    
    def get_severity_level(self, score):
        """Get severity level based on score."""
        scoring_config = settings.ASSESSMENT_SETTINGS.get(f"{self.short_name}_SCORING", {})
        
        for level, (min_score, max_score) in scoring_config.items():
            if min_score <= score <= max_score:
                return level.replace('_', ' ').title()
        
        return "Unknown"
    
    def get_severity_color(self, score):
        """Get color code for severity level."""
        level = self.get_severity_level(score).lower().replace(' ', '_')
        colors = {
            'minimal': 'green',
            'mild': 'yellow',
            'moderate': 'orange',
            'moderately_severe': 'red',
            'severe': 'red'
        }
        return colors.get(level, 'gray')


class Question(models.Model):
    """Questions for different assessments."""
    
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    order = models.PositiveIntegerField()
    
    # Question configuration
    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['assessment_type', 'order']
        unique_together = ['assessment_type', 'order']
    
    def __str__(self):
        return f"{self.assessment_type.short_name} Q{self.order}: {self.question_text[:50]}..."


class AnswerChoice(models.Model):
    """Answer choices for questions."""
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_choices')
    choice_text = models.CharField(max_length=200)
    score_value = models.IntegerField()
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['question', 'order']
        unique_together = ['question', 'order']
    
    def __str__(self):
        return f"{self.choice_text} (Score: {self.score_value})"


class Assessment(models.Model):
    """User's assessment session."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assessments')
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
    
    # Session data
    session_key = models.CharField(max_length=40, null=True, blank=True, help_text="For anonymous users")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    # Assessment status
    status = models.CharField(
        max_length=20,
        choices=[
            ('started', 'Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('abandoned', 'Abandoned'),
        ],
        default='started'
    )
    
    # Scoring
    total_score = models.IntegerField(null=True, blank=True)
    severity_level = models.CharField(max_length=50, blank=True)
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.DurationField(null=True, blank=True, help_text="Time taken to complete")
    
    # Privacy
    is_anonymous = models.BooleanField(default=False)
    share_results = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        user_info = self.user.email if self.user else "Anonymous"
        return f"{self.assessment_type.short_name} - {user_info} - {self.started_at.date()}"
    
    def calculate_score(self):
        """Calculate total score from all answers."""
        total = sum(answer.selected_choice.score_value for answer in self.answers.all())
        self.total_score = total
        self.severity_level = self.assessment_type.get_severity_level(total)
        return total
    
    def mark_completed(self):
        """Mark assessment as completed and calculate final metrics."""
        self.completed_at = timezone.now()
        self.time_taken = self.completed_at - self.started_at
        self.status = 'completed'
        self.calculate_score()
        self.save()
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage."""
        total_questions = self.assessment_type.questions.filter(is_active=True).count()
        answered_questions = self.answers.count()
        
        if total_questions == 0:
            return 0
        
        return round((answered_questions / total_questions) * 100, 1)
    
    @property
    def is_complete(self):
        """Check if assessment is complete."""
        return self.completion_percentage == 100.0
    
    def get_guidance(self):
        """Get guidance based on assessment results."""
        if not self.total_score:
            return {}
        
        severity = self.severity_level.lower().replace(' ', '_')
        
        guidance_map = {
            'minimal': {
                'title': 'Minimal Symptoms',
                'message': 'Your responses suggest minimal symptoms. Continue maintaining your mental wellness!',
                'recommendations': [
                    'Continue with regular self-care practices',
                    'Maintain social connections',
                    'Keep up with physical exercise',
                    'Practice stress management techniques'
                ],
                'urgency': 'low',
                'color': 'green'
            },
            'mild': {
                'title': 'Mild Symptoms',
                'message': 'Your responses suggest mild symptoms that may benefit from attention and care.',
                'recommendations': [
                    'Consider talking to a mental health professional',
                    'Practice mindfulness and relaxation techniques',
                    'Maintain regular sleep schedule',
                    'Engage in enjoyable activities',
                    'Consider joining support groups'
                ],
                'urgency': 'medium',
                'color': 'yellow'
            },
            'moderate': {
                'title': 'Moderate Symptoms',
                'message': 'Your responses suggest moderate symptoms. Professional support is recommended.',
                'recommendations': [
                    'Schedule an appointment with a mental health professional',
                    'Consider therapy or counseling',
                    'Talk to your primary care doctor',
                    'Reach out to trusted friends or family',
                    'Use crisis resources if needed'
                ],
                'urgency': 'high',
                'color': 'orange'
            },
            'severe': {
                'title': 'Severe Symptoms',
                'message': 'Your responses suggest severe symptoms. Immediate professional help is strongly recommended.',
                'recommendations': [
                    'Seek immediate professional help',
                    'Contact a mental health crisis line',
                    'Consider emergency services if in immediate danger',
                    'Inform a trusted person about your situation',
                    'Do not wait - help is available'
                ],
                'urgency': 'critical',
                'color': 'red'
            }
        }
        
        return guidance_map.get(severity, guidance_map['minimal'])


class Answer(models.Model):
    """User's answer to a specific question."""
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE)
    
    # Metadata
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['assessment', 'question']
        ordering = ['question__order']
    
    def __str__(self):
        return f"{self.assessment} - Q{self.question.order}: {self.selected_choice.choice_text}"


class AssessmentResult(models.Model):
    """Detailed results and analytics for completed assessments."""
    
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='result')
    
    # Detailed scoring
    raw_scores = models.JSONField(default=dict, help_text="Raw scores per question")
    subscale_scores = models.JSONField(default=dict, help_text="Subscale scores if applicable")
    percentile_rank = models.FloatField(null=True, blank=True)
    
    # Recommendations
    recommendations = models.JSONField(default=list)
    resources_suggested = models.JSONField(default=list)
    
    # Follow-up
    follow_up_recommended = models.BooleanField(default=False)
    follow_up_timeframe = models.CharField(
        max_length=20,
        choices=[
            ('immediately', 'Immediately'),
            ('within_24h', 'Within 24 hours'),
            ('within_week', 'Within a week'),
            ('within_month', 'Within a month'),
        ],
        blank=True
    )
    
    # Metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Results for {self.assessment}"


class EmergencyResource(models.Model):
    """Emergency mental health resources."""
    
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    availability = models.CharField(max_length=100, default="24/7")
    country = models.CharField(max_length=50, default="US")
    is_crisis_line = models.BooleanField(default=True)
    
    # Display settings
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=1, help_text="Lower numbers = higher priority")
    
    class Meta:
        ordering = ['priority', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.phone_number}"
