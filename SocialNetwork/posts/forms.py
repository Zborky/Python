from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label="Hashtagy",
        help_text="Zadaj tagy ako napr. #fun #Sranda",
        widget=forms.TextInput(attrs={
            'placeholder': '#fun #python',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Post
        fields = ['content', 'image', 'tags_input', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Daj príspevok...',
                'rows': 3,
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
