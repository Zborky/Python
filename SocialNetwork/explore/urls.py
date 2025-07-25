from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.global_search, name='global_search'),
    path('search/suggestions/', views.ajax_search_suggestions, name='ajax_search_suggestions'),
]