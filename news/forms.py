from django import forms
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'intro', 'body', 'tags']

