from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Article, Comment
from .forms import CommentForm


class ArticleListView(ListView):
    queryset = Article.objects.filter(is_published=True)
    template_name = 'article_list.html' 
    paginate_by = 10


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.article_comments.filter(is_visible=True)
        context['comment_form'] = CommentForm()
        return context


class UpdateCommentView(View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        author = request.user
        
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(author=author, article=article, body=form.cleaned_data['body'])

        return redirect(article)
