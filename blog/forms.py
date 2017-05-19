from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """A form to create new posts"""
    class Meta:
        model = Post
        fields = ('title', 'text')