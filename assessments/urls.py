from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    # Assessment list and details
    path('', views.AssessmentListView.as_view(), name='list'),
    path('<str:short_name>/', views.AssessmentDetailView.as_view(), name='detail'),
    path('<str:short_name>/take/', views.AssessmentTakeView.as_view(), name='take'),
    
    # Assessment results and history
    path('result/<uuid:assessment_id>/', views.AssessmentResultView.as_view(), name='result'),
    path('history/', views.UserAssessmentHistoryView.as_view(), name='history'),
    
    # Emergency resources
    path('help/emergency/', views.EmergencyResourcesView.as_view(), name='emergency'),
    
    # API endpoints
    path('api/<str:short_name>/questions/', views.assessment_questions_api, name='questions_api'),
    path('api/<uuid:assessment_id>/progress/', views.AssessmentProgressView.as_view(), name='progress_api'),
]
