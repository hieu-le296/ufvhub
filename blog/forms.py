from .models import Post, Comment
from django import forms
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'text': SummernoteWidget(),
        }
