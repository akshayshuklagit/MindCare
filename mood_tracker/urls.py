from django.urls import path
from . import views

app_name = 'mood_tracker'

urlpatterns = [
    path('', views.mood_tracker_home, name='home'),
    path('log/', views.log_mood, name='log'),
    path('history/', views.mood_history, name='history'),
    path('analytics/', views.mood_analytics, name='analytics'),
]