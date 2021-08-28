from django import forms
from .models import Blog, Comment

class BlogForm(forms.ModelForm):
    tag = forms.CharField(required = False, label = "태그")
    class Meta:
        model = Blog
        fields = ['title', 'writer', 'body', 'image']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
