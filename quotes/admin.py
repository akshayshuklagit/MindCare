from django.contrib import admin
from .models import Quote, UserFavoriteQuote, DailyQuote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'author', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['text', 'author']
    list_editable = ['is_active']
    
    def text_preview(self, obj):
        return f"{obj.text[:50]}..."
    text_preview.short_description = 'Quote'

@admin.register(UserFavoriteQuote)
class UserFavoriteQuoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'quote_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'quote__text']
    
    def quote_preview(self, obj):
        return f"{obj.quote.text[:30]}..."
    quote_preview.short_description = 'Quote'

@admin.register(DailyQuote)
class DailyQuoteAdmin(admin.ModelAdmin):
    list_display = ['date', 'quote_preview', 'created_at']
    list_filter = ['date']
    
    def quote_preview(self, obj):
        return f"{obj.quote.text[:30]}..."
    quote_preview.short_description = 'Quote'