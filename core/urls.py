from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('breathing/', views.breathing_exercise, name='breathing'),
    path('coloring/', views.coloring_game, name='coloring'),
    path('gratitude/', views.gratitude_jar, name='gratitude_jar'),
    path('gratitude/history/', views.gratitude_history, name='gratitude_history'),
    path('emotion-wheel/', views.emotion_wheel, name='emotion_wheel'),
]