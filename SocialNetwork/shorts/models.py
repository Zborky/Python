from django.db import models

from django.contrib.auth.models import User

class Short(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.FileField(upload_to='shorts_videos/')
    caption = models.CharField(max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Short by {self.user.username}"
    def total_likes(self):
        return self.likes.count()
    
class ShortLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    short = models.ForeignKey(Short,related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','short')
        
    def __str__(self):
        return f"{self.user} liked {self.short}"
    
class ShortComment(models.Model):
    short = models.ForeignKey('Short', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text[:30]}"      