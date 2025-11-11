from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('goals/', views.goals_list, name='goals'),
    path('goals/create/', views.create_goal, name='create_goal'),
    path('goals/<int:goal_id>/update/', views.update_goal_progress, name='update_goal'),
]