from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from quotes.models import Quote
from .models import GratitudeEntry
import random
from datetime import datetime, timedelta

def home(request):
    # Get 1 random Bhagavad Gita quote
    gita_quotes = Quote.objects.filter(is_active=True, category='mindfulness').order_by('?')[:1]
    if not gita_quotes:
        gita_quotes = Quote.objects.filter(is_active=True).order_by('?')[:1]
    
    context = {
        'gita_quotes': gita_quotes,
    }
    return render(request, 'core/home.html', context)

def breathing_exercise(request):
    return render(request, 'core/breathing.html')

def coloring_game(request):
    return render(request, 'core/coloring.html')

@login_required
def gratitude_jar(request):
    today = timezone.now().date()
    user_entries = GratitudeEntry.objects.filter(user=request.user)
    today_entry = user_entries.filter(date=today).first()
    total_entries = user_entries.count()
    
    # Get weekly highlights (last 7 days)
    week_ago = today - timedelta(days=7)
    weekly_entries = user_entries.filter(date__gte=week_ago)[:7]
    
    if request.method == 'POST':
        if not today_entry:
            content = request.POST.get('gratitude_content', '').strip()
            if content:
                GratitudeEntry.objects.create(
                    user=request.user,
                    content=content,
                    date=today
                )
                messages.success(request, 'Your gratitude has been added to the jar!')
                return redirect('core:gratitude_jar')
            else:
                messages.error(request, 'Please write something you are grateful for.')
        else:
            messages.info(request, 'You have already added your gratitude for today!')
    
    context = {
        'today_entry': today_entry,
        'total_entries': total_entries,
        'weekly_entries': weekly_entries,
        'can_add_today': not today_entry,
    }
    return render(request, 'core/gratitude_jar.html', context)

@login_required
def gratitude_history(request):
    entries = GratitudeEntry.objects.filter(user=request.user)[:30]
    context = {'entries': entries}
    return render(request, 'core/gratitude_history.html', context)

def emotion_wheel(request):
    return render(request, 'core/emotion_wheel.html')