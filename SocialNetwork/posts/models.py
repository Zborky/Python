from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .hate_detector import is_hate_speech
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    video = models.FileField(upload_to='post_videos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'Post by {self.user.username} - {self.created_at.strftime("%d.%m.%Y %H:%M")}'
    
    def clean(self,*args,**kwargs):
        if is_hate_speech(self.content):
            raise ValidationError("Tento prispevok obsahuje nevhodny obsah")
    
    def save(self, *args,**kwargs):
        self.full_clean()
        super().save(*args, **kwargs)    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_objects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} liked Post {self.post.id}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f'{self.user.username} commented on Post {self.post.id}'


