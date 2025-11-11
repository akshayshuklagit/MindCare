from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class ResourceCategory(models.Model):
    """Categories for organizing resources."""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-book', help_text="FontAwesome icon class")
    color = models.CharField(max_length=20, default='blue', help_text="Color theme for category")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Resource Categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('resources:category', kwargs={'slug': self.slug})


class Resource(models.Model):
    """Mental health resources, articles, and tools."""
    
    RESOURCE_TYPES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('tool', 'Interactive Tool'),
        ('worksheet', 'Worksheet'),
        ('guide', 'Guide'),
        ('external', 'External Link'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='article')
    
    # Content
    summary = models.TextField(help_text="Brief description of the resource")
    content = models.TextField(blank=True, help_text="Full content for articles/guides")
    external_url = models.URLField(blank=True, help_text="External link for videos/tools")
    
    # Metadata
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    estimated_read_time = models.PositiveIntegerField(default=5, help_text="Estimated time in minutes")
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # Engagement
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-is_featured', '-published_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('resources:detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Return tags as a list."""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def increment_view_count(self):
        """Increment view count."""
        self.view_count += 1
        self.save(update_fields=['view_count'])





class CrisisResource(models.Model):
    """Crisis intervention and emergency resources."""
    
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    text_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField()
    
    # Availability
    availability = models.CharField(max_length=100, default="24/7")
    country = models.CharField(max_length=50, default="US")
    
    # Categorization
    is_crisis_line = models.BooleanField(default=True)
    is_text_support = models.BooleanField(default=False)
    is_chat_support = models.BooleanField(default=False)
    
    # Display
    priority = models.PositiveIntegerField(default=1, help_text="Lower numbers = higher priority")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.phone_number}"


