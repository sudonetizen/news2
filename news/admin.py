from django.contrib import admin
from .models import Article, Comment, Like, Read

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'intro', 'publish', 'is_published']
    list_filter = ['is_published', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'body', 'is_visible']
    list_filter = ['is_visible', 'created', 'updated']
    search_fields = ['author', 'body']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['author', 'article', 'created', 'updated']
    list_filter = ['author', 'article']
    search_fields = ['author', 'article']

@admin.register(Read)
class ReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'created', 'updated']
    list_filter = ['user', 'article']
    search_fields = ['user', 'article']
