from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article


class ArticleListView(ListView):
    queryset = Article.objects.filter(is_published=True)
    template_name = 'article_list.html' 


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
