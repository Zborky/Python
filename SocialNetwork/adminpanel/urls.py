from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
