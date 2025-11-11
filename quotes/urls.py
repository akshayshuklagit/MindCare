from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quote_list, name='list'),
    path('daily/', views.daily_quote, name='daily'),
    path('favorites/', views.favorite_quotes, name='favorites'),
    path('toggle-favorite/<int:quote_id>/', views.toggle_favorite, name='toggle_favorite'),
]