from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shorts/', include('shorts.urls')),
    path('', include('feed.urls')),  # hlavná stránka bude feed
    path('users/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('stories/', include('stories.urls')),
    path('chat/', include('chat.urls')),
    path('', include('users.urls')),
    path('explore/', include('explore.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]
