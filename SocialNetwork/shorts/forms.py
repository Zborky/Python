from django import forms
from .models import Short
from .models import ShortComment
class ShortForm(forms.ModelForm):
    class Meta:
        model = Short
        fields = ['video', 'caption']
        
class ShortCommentForm(forms.ModelForm):
    class Meta:
        model = ShortComment  
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Napis komentar...'})
        }