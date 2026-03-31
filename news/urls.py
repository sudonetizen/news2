from django.urls import path
from .views import ArticleListView, ArticleDetailView, UpdateCommentView, search_article, search_tag

app_name = 'news'

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("<slug:slug>/tag/", search_tag, name="tag_search"),
    path("search/", search_article, name="article_search"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<slug:slug>/add_comment/", UpdateCommentView.as_view(), name="add_comment"),
]

