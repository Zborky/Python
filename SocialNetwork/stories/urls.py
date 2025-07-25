from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.story_upload, name='story-upload'),
    path('<str:username>/', views.view_story, name='view-story'),
    path('<str:username>/<int:index>/', views.view_story, name='view-story-index'),
]