from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    
    def __str__(self):
        return f'{self.user.username}'
