from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add-comment'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit-comment'),
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete-comment'),
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
    path('gallery/<str:username>/', views.user_gallery, name='user-gallery'),
    path('ajax/comment/<int:post_id>/', views.ajax_add_comment, name='ajax-add-comment'),
]