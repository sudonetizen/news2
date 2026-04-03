from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.db.models import Q
from .models import Article, Comment, Like
from .forms import CommentForm, ArticleForm


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


class ArticleDetailView(UserPassesTestMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

    def test_func(self):
        is_mod = self.request.user.groups.filter(name='moderators').exists()
        is_wrt = self.request.user.groups.filter(name='writers').exists()
        obj = self.get_object()

        if obj.is_published == True:
            return True
        elif obj.is_published == False and (is_mod or is_wrt):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.article_comments.filter(is_visible=True)
        context['comment_form'] = CommentForm()
        return context


class UpdateCommentView(LoginRequiredMixin, View):
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
        intro_search = Q(intro__icontains=query)
        tag_search = Q(tags__icontains=query)
        published_articles = Article.objects.filter(is_published=True)
        results = published_articles.filter(title_search | body_search | tag_search | intro_search )
    
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


class UpdateLikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        author = request.user 
    
        try: Like.objects.create(article=article, author=author)
        except:
            obj = Like.objects.get(article=article, author=author)
            obj.delete()

        return redirect(article)

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='writers').exists()        

    def get(self, request):
        sent = False
        form = ArticleForm()

        return render(request, 'article_form.html', {'sent':sent, 'form': form})

    def post(self, request):
        sent = True
        form = ArticleForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            Article.objects.create(
                author=request.user,
                title=cd['title'],
                intro=cd['intro'],
                body=cd['body'],
                tags=cd['tags'],
                slug=cd['slug']
            )

        return render(request, 'article_form.html', {'sent': sent})


class ArticleModerateListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = Article.objects.filter(is_published=False)
    template_name = "article_moderate_list.html"

    def test_func(self):
        return self.request.user.groups.filter(name='moderators').exists()        

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'slug', 'intro', 'body', 'tags']
    template_name = "article_edit.html"

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user:
            return True
        elif self.request.user.groups.filter(name='moderators').exists():
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user or self.request.user.groups.filter(name='moderators').exists():
            return True
        return False


class UserArticleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='writers').exists()        

    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        
        return render(request, 'user_articles.html', {'articles':articles})

class ArticleApproveView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='moderators').exists()        

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        article.is_published = True
        article.article_comments.all().delete()
        article.save()

        return redirect("news:article_list")
