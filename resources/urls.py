from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    # Main resources
    path('', views.ResourceListView.as_view(), name='list'),
    path('resource/<slug:slug>/', views.ResourceDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryResourcesView.as_view(), name='category'),
    

    
    # Crisis resources
    path('crisis/', views.CrisisResourcesView.as_view(), name='crisis'),
    

]