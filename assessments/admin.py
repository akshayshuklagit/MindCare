from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Avg
from .models import (
    AssessmentType, Question, AnswerChoice, Assessment, 
    Answer, AssessmentResult, EmergencyResource
)


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4
    fields = ('choice_text', 'score_value', 'order')
    ordering = ['order']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    fields = ('question_text', 'order', 'is_required', 'is_active')
    ordering = ['order']


@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'short_name', 'max_score', 'estimated_time', 
        'question_count', 'assessment_count', 'is_active'
    ]
    list_filter = ['is_active', 'requires_login', 'scoring_method']
    search_fields = ['name', 'short_name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_name', 'description', 'instruction')
        }),
        ('Scoring Configuration', {
            'fields': ('max_score', 'scoring_method')
        }),
        ('Settings', {
            'fields': ('is_active', 'requires_login', 'estimated_time')
        }),
    )
    
    inlines = [QuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'
    
    def assessment_count(self, obj):
        return obj.assessment_set.count()
    assessment_count.short_description = 'Assessments Taken'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'assessment_type', 'order', 'answer_count', 'is_active']
    list_filter = ['assessment_type', 'is_active', 'is_required']
    search_fields = ['question_text']
    ordering = ['assessment_type', 'order']
    
    inlines = [AnswerChoiceInline]
    
    def question_preview(self, obj):
        return f"{obj.question_text[:80]}..."
    question_preview.short_description = 'Question'
    
    def answer_count(self, obj):
        return obj.answer_choices.count()
    answer_count.short_description = 'Answer Choices'


@admin.register(AnswerChoice)
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question_preview', 'score_value', 'order']
    list_filter = ['question__assessment_type']
    search_fields = ['choice_text', 'question__question_text']
    
    def question_preview(self, obj):
        return f"{obj.question.question_text[:50]}..."
    question_preview.short_description = 'Question'


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ['question', 'selected_choice', 'answered_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'assessment_id', 'user_info', 'assessment_type', 'status', 
        'completion_percentage', 'total_score', 'severity_level', 'started_at'
    ]
    list_filter = [
        'status', 'assessment_type', 'severity_level', 
        'is_anonymous', 'started_at'
    ]
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'session_key']
    readonly_fields = [
        'id', 'started_at', 'completed_at', 'time_taken', 
        'completion_percentage', 'total_score', 'severity_level'
    ]
    
    fieldsets = (
        ('Assessment Info', {
            'fields': ('id', 'user', 'assessment_type', 'status')
        }),
        ('Session Data', {
            'fields': ('session_key', 'ip_address', 'user_agent', 'is_anonymous')
        }),
        ('Results', {
            'fields': ('total_score', 'severity_level', 'completion_percentage')
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'time_taken')
        }),
        ('Privacy', {
            'fields': ('share_results',)
        }),
    )
    
    inlines = [AnswerInline]
    
    def assessment_id(self, obj):
        return str(obj.id)[:8]
    assessment_id.short_description = 'ID'
    
    def user_info(self, obj):
        if obj.user:
            return obj.user.email
        return "Anonymous User"
    user_info.short_description = 'User'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'assessment_type')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['assessment_info', 'question_preview', 'selected_choice', 'score', 'answered_at']
    list_filter = ['question__assessment_type', 'answered_at']
    search_fields = ['assessment__user__email', 'question__question_text']
    readonly_fields = ['assessment', 'question', 'selected_choice', 'answered_at']
    
    def assessment_info(self, obj):
        return f"{obj.assessment.assessment_type.short_name} - {obj.assessment.user_info if hasattr(obj.assessment, 'user_info') else 'Anonymous'}"
    assessment_info.short_description = 'Assessment'
    
    def question_preview(self, obj):
        return f"Q{obj.question.order}: {obj.question.question_text[:40]}..."
    question_preview.short_description = 'Question'
    
    def score(self, obj):
        return obj.selected_choice.score_value
    score.short_description = 'Score'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ['assessment_info', 'total_score', 'percentile_rank', 'follow_up_recommended', 'generated_at']
    list_filter = ['follow_up_recommended', 'follow_up_timeframe', 'generated_at']
    search_fields = ['assessment__user__email']
    readonly_fields = ['assessment', 'generated_at']
    
    fieldsets = (
        ('Assessment Info', {
            'fields': ('assessment', 'generated_at')
        }),
        ('Scoring Details', {
            'fields': ('raw_scores', 'subscale_scores', 'percentile_rank')
        }),
        ('Recommendations', {
            'fields': ('recommendations', 'resources_suggested')
        }),
        ('Follow-up', {
            'fields': ('follow_up_recommended', 'follow_up_timeframe')
        }),
    )
    
    def assessment_info(self, obj):
        return str(obj.assessment)
    assessment_info.short_description = 'Assessment'
    
    def total_score(self, obj):
        return obj.assessment.total_score
    total_score.short_description = 'Total Score'


@admin.register(EmergencyResource)
class EmergencyResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'country', 'availability', 'is_crisis_line', 'priority', 'is_active']
    list_filter = ['country', 'is_crisis_line', 'is_active']
    search_fields = ['name', 'phone_number', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'phone_number', 'description')
        }),
        ('Availability', {
            'fields': ('availability', 'country')
        }),
        ('Settings', {
            'fields': ('is_crisis_line', 'priority', 'is_active')
        }),
    )


# Add custom admin site header
admin.site.site_header = "MindCare Administration"
admin.site.site_title = "MindCare Admin"
admin.site.index_title = "Welcome to MindCare Administration"
