from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Quote, UserFavoriteQuote, DailyQuote
import random

def quote_list(request):
    category = request.GET.get('category', '')
    quotes = Quote.objects.filter(is_active=True)
    
    if category:
        quotes = quotes.filter(category=category)
    
    categories = Quote.CATEGORY_CHOICES
    
    context = {
        'quotes': quotes,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'quotes/quote_list.html', context)

def daily_quote(request):
    today = timezone.now().date()
    
    try:
        daily_quote_obj = DailyQuote.objects.get(date=today)
        quote = daily_quote_obj.quote
    except DailyQuote.DoesNotExist:
        # Select a random quote for today
        quotes = Quote.objects.filter(is_active=True)
        if quotes.exists():
            quote = random.choice(quotes)
            DailyQuote.objects.create(quote=quote, date=today)
        else:
            quote = None
    
    context = {'quote': quote}
    return render(request, 'quotes/daily_quote.html', context)

@login_required
def toggle_favorite(request, quote_id):
    if request.method == 'POST':
        quote = get_object_or_404(Quote, id=quote_id)
        favorite, created = UserFavoriteQuote.objects.get_or_create(
            user=request.user, quote=quote
        )
        
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
        
        return JsonResponse({'is_favorite': is_favorite})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def favorite_quotes(request):
    favorites = UserFavoriteQuote.objects.filter(user=request.user).select_related('quote')
    context = {'favorites': favorites}
    return render(request, 'quotes/favorites.html', context)