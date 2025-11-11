from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from .models import ResourceCategory, Resource, CrisisResource


class ResourceListView(ListView):
    """List all resources with filtering and search."""
    model = Resource
    template_name = 'resources/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(tags__icontains=search_query)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Resource type filter
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        
        # Difficulty filter
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ResourceCategory.objects.filter(is_active=True)
        context['resource_types'] = Resource.RESOURCE_TYPES
        context['difficulty_levels'] = Resource.DIFFICULTY_LEVELS
        context['featured_resources'] = Resource.objects.filter(is_featured=True, is_active=True)[:3]
        
        # Current filters
        context['current_search'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['current_difficulty'] = self.request.GET.get('difficulty', '')
        
        return context


class ResourceDetailView(DetailView):
    """Display detailed resource view."""
    model = Resource
    template_name = 'resources/resource_detail.html'
    context_object_name = 'resource'
    
    def get_queryset(self):
        return Resource.objects.filter(is_active=True).select_related('category')
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_view_count()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.get_object()
        
        # Related resources
        context['related_resources'] = Resource.objects.filter(
            category=resource.category,
            is_active=True
        ).exclude(id=resource.id)[:3]
        
        return context


class CategoryResourcesView(ListView):
    """List resources by category."""
    model = Resource
    template_name = 'resources/category_resources.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(ResourceCategory, slug=self.kwargs['slug'], is_active=True)
        return Resource.objects.filter(category=self.category, is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context





class CrisisResourcesView(ListView):
    """Display crisis and emergency resources."""
    model = CrisisResource
    template_name = 'resources/crisis_resources.html'
    context_object_name = 'crisis_resources'
    
    def get_queryset(self):
        return CrisisResource.objects.filter(is_active=True).order_by('priority', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crisis_lines'] = self.get_queryset().filter(is_crisis_line=True)
        context['text_support'] = self.get_queryset().filter(is_text_support=True)
        context['chat_support'] = self.get_queryset().filter(is_chat_support=True)
        return context


