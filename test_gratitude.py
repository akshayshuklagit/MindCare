#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindcare_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import GratitudeEntry
from django.utils import timezone

def test_gratitude_jar():
    print("Testing Gratitude Jar functionality...")
    
    # Create a test user if it doesn't exist
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'first_name': 'Test'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing user: {user.username}")
    
    # Test creating a gratitude entry
    today = timezone.now().date()
    entry, created = GratitudeEntry.objects.get_or_create(
        user=user,
        date=today,
        defaults={'content': 'I am grateful for this beautiful day and the opportunity to practice gratitude.'}
    )
    
    if created:
        print(f"Created gratitude entry: {entry.content[:50]}...")
    else:
        print(f"Entry already exists for today: {entry.content[:50]}...")
    
    # Test retrieving entries
    total_entries = GratitudeEntry.objects.filter(user=user).count()
    print(f"Total gratitude entries for {user.username}: {total_entries}")
    
    # Test weekly entries
    from datetime import timedelta
    week_ago = today - timedelta(days=7)
    weekly_entries = GratitudeEntry.objects.filter(user=user, date__gte=week_ago).count()
    print(f"Entries in the last 7 days: {weekly_entries}")
    
    print("Gratitude Jar functionality test completed successfully!")
    
    # Print URLs for testing
    print("\nTo test the gratitude jar, visit these URLs after starting the server:")
    print("- http://127.0.0.1:8000/gratitude/ (Main gratitude jar)")
    print("- http://127.0.0.1:8000/gratitude/history/ (Gratitude history)")
    print("- http://127.0.0.1:8000/ (Home page with gratitude jar link)")

if __name__ == '__main__':
    test_gratitude_jar()