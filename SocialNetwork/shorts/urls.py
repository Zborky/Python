from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_short, name='upload_short'),
    path('feed/', views.shorts_feed, name='shorts_feed'),
    path('like/<int:short_id>/', views.like_short, name='like_short'),
    path('comment/<int:short_id>/', views.add_short_comment, name='add_short_comment'),
    

]
