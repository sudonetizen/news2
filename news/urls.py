from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView, 
    UpdateCommentView, 
    search_article, 
    search_tag, 
    UpdateLikeView,
    ArticleCreateView,
    ArticleModerateListView,
)

app_name = 'news'

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("<slug:slug>/tag/", search_tag, name="tag_search"),
    path("search/", search_article, name="article_search"),
    path("moderate/", ArticleModerateListView.as_view(), name="article_moderate"),
    path("article/new/", ArticleCreateView.as_view(), name="article_new"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<slug:slug>/add_comment/", UpdateCommentView.as_view(), name="add_comment"),
    path("<slug:slug>/add_like/", UpdateLikeView.as_view(), name="add_like"),
]

