from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.db.models import Q
from .models import Article, Comment, Like
from .forms import CommentForm


class ArticleListView(ListView):
    queryset = Article.objects.filter(is_published=True)
    template_name = 'article_list.html' 
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        articles = self.get_queryset()
        unique_tags = set()
        for article in articles:
            for tag in article.tags:
                unique_tags.add(tag)    

        context['unique_tags'] = unique_tags
        return context


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

def search_article(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        title_search = Q(title__icontains=query)
        body_search = Q(body__icontains=query)
        tag_search = Q(tags__icontains=query)
        published_articles = Article.objects.filter(is_published=True)
        results = published_articles.filter(title_search | body_search | tag_search )
    
    return render(request, 'search_list.html', {'search_results': results})


def search_tag(request, slug):
    query = request.GET.get("q", "").strip()
    published_articles = Article.objects.filter(is_published=True)
    results = []

    if query:
        tag_search = Q(tags__icontains=query)

        if slug:
            published_articles = published_articles.exclude(slug=slug)

        results = published_articles.filter(tag_search)

    return render(request, 'search_tag.html', {'search_results': results})


class UpdateLikeView(View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        author = request.user 
    
        try: Like.objects.create(article=article, author=author)
        except:
            obj = Like.objects.get(article=article, author=author)
            obj.delete()

        return redirect(article)
