from django.urls import path
from . import views

urlpatterns = [
     path('inbox/', views.inbox_view, name='inbox'),
    path('<str:username>/', views.chat_view, name='chat'),
    path('<str:username>/private/', views.private_chat, name='private-chat'),
]