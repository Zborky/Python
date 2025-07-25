from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/', blank= True, null = True)
    video = models.FileField(upload_to='stories/',blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        return timezone.now() < self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"Story by {self.user.username}"
