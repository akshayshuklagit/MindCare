from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg
from django.http import JsonResponse
from .models import MoodEntry, MoodTrigger
from datetime import datetime, timedelta
import json

@login_required
def mood_tracker_home(request):
    today = timezone.now().date()
    
    # Check if user already logged mood today
    today_entry = MoodEntry.objects.filter(user=request.user, date=today).first()
    
    # Get recent entries for chart
    recent_entries = MoodEntry.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=30)
    ).order_by('date')
    
    # Calculate averages
    avg_mood = MoodEntry.objects.filter(user=request.user).aggregate(
        avg_mood=Avg('mood_rating'),
        avg_energy=Avg('energy_level'),
        avg_anxiety=Avg('anxiety_level')
    )
    
    context = {
        'today_entry': today_entry,
        'recent_entries': recent_entries,
        'avg_mood': avg_mood,
    }
    return render(request, 'mood_tracker/home.html', context)

@login_required
def log_mood(request):
    today = timezone.now().date()
    
    # Check if already logged today
    existing_entry = MoodEntry.objects.filter(user=request.user, date=today).first()
    
    if request.method == 'POST':
        mood_rating = request.POST.get('mood_rating')
        energy_level = request.POST.get('energy_level')
        anxiety_level = request.POST.get('anxiety_level')
        sleep_hours = request.POST.get('sleep_hours')
        notes = request.POST.get('notes', '')
        
        if existing_entry:
            # Update existing entry
            existing_entry.mood_rating = mood_rating
            existing_entry.energy_level = energy_level
            existing_entry.anxiety_level = anxiety_level
            existing_entry.sleep_hours = sleep_hours if sleep_hours else None
            existing_entry.notes = notes
            existing_entry.save()
            messages.success(request, 'Mood entry updated successfully!')
        else:
            # Create new entry
            MoodEntry.objects.create(
                user=request.user,
                mood_rating=mood_rating,
                energy_level=energy_level,
                anxiety_level=anxiety_level,
                sleep_hours=sleep_hours if sleep_hours else None,
                notes=notes,
                date=today
            )
            messages.success(request, 'Mood logged successfully!')
        
        return redirect('mood_tracker:home')
    
    triggers = MoodTrigger.objects.all()
    context = {
        'existing_entry': existing_entry,
        'triggers': triggers,
        'mood_choices': MoodEntry.MOOD_CHOICES,
        'energy_choices': MoodEntry.ENERGY_CHOICES,
    }
    return render(request, 'mood_tracker/log_mood.html', context)

@login_required
def mood_history(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by('-date')
    
    # Pagination could be added here
    context = {'entries': entries}
    return render(request, 'mood_tracker/history.html', context)

@login_required
def mood_analytics(request):
    # Get data for the last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    entries = MoodEntry.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # Prepare data for charts
    chart_data = {
        'dates': [entry.date.strftime('%Y-%m-%d') for entry in entries],
        'mood_ratings': [entry.mood_rating for entry in entries],
        'energy_levels': [entry.energy_level for entry in entries],
        'anxiety_levels': [entry.anxiety_level for entry in entries],
    }
    
    context = {
        'entries': entries,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'mood_tracker/analytics.html', context)