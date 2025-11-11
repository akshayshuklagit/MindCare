from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg
from .models import UserGoal, DashboardWidget
from mood_tracker.models import MoodEntry
from quotes.models import DailyQuote
from assessments.models import Assessment
from datetime import timedelta
import json

@login_required
def dashboard_home(request):
    today = timezone.now().date()
    
    # Get user's widgets
    widgets = DashboardWidget.objects.filter(user=request.user, is_visible=True)
    
    # Dashboard data
    context_data = {}
    
    # Recent mood entries
    recent_moods = MoodEntry.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=7)
    ).order_by('-date')[:5]
    
    # Active goals
    active_goals = UserGoal.objects.filter(user=request.user, status='active')
    
    # Daily quote
    try:
        daily_quote = DailyQuote.objects.get(date=today).quote
    except DailyQuote.DoesNotExist:
        daily_quote = None
    
    # Recent assessments
    recent_assessments = Assessment.objects.filter(
        user=request.user,
        status='completed'
    ).order_by('-completed_at')[:3]
    
    # Mood streak
    mood_streak = calculate_mood_streak(request.user)
    
    context = {
        'widgets': widgets,
        'recent_moods': recent_moods,
        'active_goals': active_goals,
        'daily_quote': daily_quote,
        'recent_assessments': recent_assessments,
        'mood_streak': mood_streak,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
def goals_list(request):
    goals = UserGoal.objects.filter(user=request.user)
    context = {'goals': goals}
    return render(request, 'dashboard/goals.html', context)

@login_required
def create_goal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        goal_type = request.POST.get('goal_type')
        target_value = request.POST.get('target_value')
        target_date = request.POST.get('target_date')
        
        UserGoal.objects.create(
            user=request.user,
            title=title,
            description=description,
            goal_type=goal_type,
            target_value=int(target_value),
            target_date=target_date
        )
        
        messages.success(request, 'Goal created successfully!')
        return redirect('dashboard:goals')
    
    context = {'goal_types': UserGoal.GOAL_TYPES}
    return render(request, 'dashboard/create_goal.html', context)

@login_required
def update_goal_progress(request, goal_id):
    goal = get_object_or_404(UserGoal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        progress = int(request.POST.get('progress', 0))
        goal.current_progress = min(progress, goal.target_value)
        
        if goal.current_progress >= goal.target_value:
            goal.status = 'completed'
        
        goal.save()
        messages.success(request, 'Goal progress updated!')
    
    return redirect('dashboard:goals')

def calculate_mood_streak(user):
    """Calculate consecutive days of mood logging"""
    today = timezone.now().date()
    streak = 0
    current_date = today
    
    while True:
        if MoodEntry.objects.filter(user=user, date=current_date).exists():
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak