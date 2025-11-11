from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.db import transaction, models
from django.utils import timezone
from django.core.paginator import Paginator
import json

from .models import (
    AssessmentType, Assessment, Question, Answer, 
    AnswerChoice, AssessmentResult, EmergencyResource
)


class AssessmentListView(ListView):
    """List all available assessments."""
    model = AssessmentType
    template_name = 'assessments/assessment_list.html'
    context_object_name = 'assessments'
    
    def get_queryset(self):
        return AssessmentType.objects.filter(is_active=True).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mental Health Assessments'
        context['page_description'] = 'Take evidence-based mental health assessments to understand your current well-being.'
        return context


class AssessmentDetailView(DetailView):
    """Show assessment details and start page."""
    model = AssessmentType
    template_name = 'assessments/assessment_detail.html'
    context_object_name = 'assessment'
    slug_field = 'short_name'
    slug_url_kwarg = 'short_name'
    
    def get_queryset(self):
        return AssessmentType.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment = self.get_object()
        
        # Check if user has recent assessments
        if self.request.user.is_authenticated:
            recent_assessments = Assessment.objects.filter(
                user=self.request.user,
                assessment_type=assessment,
                status='completed'
            ).order_by('-completed_at')[:3]
            context['recent_assessments'] = recent_assessments
        
        context['question_count'] = assessment.questions.filter(is_active=True).count()
        return context


class AssessmentTakeView(View):
    """Handle taking an assessment."""
    template_name = 'assessments/assessment_take.html'
    
    def get_assessment_type(self, short_name):
        return get_object_or_404(
            AssessmentType, 
            short_name=short_name, 
            is_active=True
        )
    
    def get(self, request, short_name):
        assessment_type = self.get_assessment_type(short_name)
        
        # Create new assessment session
        assessment = Assessment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            assessment_type=assessment_type,
            session_key=request.session.session_key,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            is_anonymous=not request.user.is_authenticated
        )
        
        # Get questions
        questions = assessment_type.questions.filter(is_active=True).order_by('order')
        
        context = {
            'assessment': assessment,
            'assessment_type': assessment_type,
            'questions': questions,
            'current_question_index': 1,
            'total_questions': questions.count(),
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, short_name):
        """Process assessment submission."""
        assessment_id = request.POST.get('assessment_id')
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        try:
            with transaction.atomic():
                # Process all answers
                for key, value in request.POST.items():
                    if key.startswith('question_'):
                        question_id = key.split('_')[1]
                        choice_id = value
                        
                        question = get_object_or_404(Question, id=question_id)
                        choice = get_object_or_404(AnswerChoice, id=choice_id)
                        
                        # Create or update answer
                        Answer.objects.update_or_create(
                            assessment=assessment,
                            question=question,
                            defaults={'selected_choice': choice}
                        )
                
                # Mark assessment as completed
                assessment.mark_completed()
                
                # Create assessment result
                self.create_assessment_result(assessment)
                
                messages.success(request, 'Assessment completed successfully!')
                return redirect('assessments:result', assessment_id=assessment.id)
                
        except Exception as e:
            messages.error(request, 'There was an error processing your assessment. Please try again.')
            return redirect('assessments:take', short_name=short_name)
    
    def create_assessment_result(self, assessment):
        """Create detailed assessment result."""
        guidance = assessment.get_guidance()
        
        # Get emergency resources if severe
        resources = []
        if guidance.get('urgency') in ['high', 'critical']:
            resources = list(
                EmergencyResource.objects.filter(
                    is_active=True,
                    country='US'
                ).order_by('priority').values(
                    'name', 'phone_number', 'description', 'availability'
                )[:3]
            )
        
        AssessmentResult.objects.create(
            assessment=assessment,
            recommendations=guidance.get('recommendations', []),
            resources_suggested=resources,
            follow_up_recommended=guidance.get('urgency') in ['high', 'critical'],
            follow_up_timeframe=(
                'immediately' if guidance.get('urgency') == 'critical'
                else 'within_week' if guidance.get('urgency') == 'high'
                else ''
            )
        )
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AssessmentResultView(DetailView):
    """Show assessment results."""
    model = Assessment
    template_name = 'assessments/assessment_result.html'
    context_object_name = 'assessment'
    pk_url_kwarg = 'assessment_id'
    
    def get_queryset(self):
        # Allow access to own assessments or anonymous sessions
        if self.request.user.is_authenticated:
            return Assessment.objects.filter(
                models.Q(user=self.request.user) |
                models.Q(session_key=self.request.session.session_key)
            )
        else:
            return Assessment.objects.filter(
                session_key=self.request.session.session_key
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment = self.get_object()
        
        context['guidance'] = assessment.get_guidance()
        context['answers'] = assessment.answers.select_related('question', 'selected_choice').order_by('question__order')
        
        # Get assessment result if exists
        try:
            context['result'] = assessment.result
        except AssessmentResult.DoesNotExist:
            context['result'] = None
        
        # Emergency resources for severe cases
        if assessment.severity_level and 'severe' in assessment.severity_level.lower():
            context['emergency_resources'] = EmergencyResource.objects.filter(
                is_active=True,
                is_crisis_line=True
            ).order_by('priority')[:3]
        
        return context


@method_decorator(login_required, name='dispatch')
class UserAssessmentHistoryView(ListView):
    """Show user's assessment history."""
    model = Assessment
    template_name = 'assessments/assessment_history.html'
    context_object_name = 'assessments'
    paginate_by = 10
    
    def get_queryset(self):
        return Assessment.objects.filter(
            user=self.request.user,
            status='completed'
        ).select_related('assessment_type').order_by('-completed_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get assessment statistics
        user_assessments = Assessment.objects.filter(
            user=self.request.user,
            status='completed'
        )
        
        context['stats'] = {
            'total_assessments': user_assessments.count(),
            'assessment_types': user_assessments.values(
                'assessment_type__name'
            ).distinct().count(),
            'latest_assessment': user_assessments.first(),
        }
        
        return context


class AssessmentProgressView(View):
    """AJAX view for assessment progress."""
    
    def get(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        # Check access permissions
        if request.user.is_authenticated:
            if assessment.user != request.user and assessment.session_key != request.session.session_key:
                return JsonResponse({'error': 'Access denied'}, status=403)
        else:
            if assessment.session_key != request.session.session_key:
                return JsonResponse({'error': 'Access denied'}, status=403)
        
        return JsonResponse({
            'status': assessment.status,
            'completion_percentage': assessment.completion_percentage,
            'total_score': assessment.total_score,
            'severity_level': assessment.severity_level,
            'questions_answered': assessment.answers.count(),
            'total_questions': assessment.assessment_type.questions.filter(is_active=True).count(),
        })


class EmergencyResourcesView(ListView):
    """List emergency mental health resources."""
    model = EmergencyResource
    template_name = 'assessments/emergency_resources.html'
    context_object_name = 'resources'
    
    def get_queryset(self):
        return EmergencyResource.objects.filter(
            is_active=True
        ).order_by('priority', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crisis_lines'] = self.get_queryset().filter(is_crisis_line=True)
        context['general_resources'] = self.get_queryset().filter(is_crisis_line=False)
        return context


# API Views for AJAX requests
def assessment_questions_api(request, short_name):
    """API endpoint to get assessment questions."""
    assessment_type = get_object_or_404(AssessmentType, short_name=short_name)
    questions = assessment_type.questions.filter(is_active=True).order_by('order')
    
    questions_data = []
    for question in questions:
        choices_data = []
        for choice in question.answer_choices.order_by('order'):
            choices_data.append({
                'id': choice.id,
                'text': choice.choice_text,
                'score': choice.score_value
            })
        
        questions_data.append({
            'id': question.id,
            'text': question.question_text,
            'order': question.order,
            'choices': choices_data
        })
    
    return JsonResponse({
        'assessment_type': {
            'id': assessment_type.id,
            'name': assessment_type.name,
            'instruction': assessment_type.instruction,
            'estimated_time': assessment_type.estimated_time
        },
        'questions': questions_data
    })
