from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'intro', 'publish', 'is_published']
    list_filter = ['is_published', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    show_facets = admin.ShowFacets.ALWAYS
