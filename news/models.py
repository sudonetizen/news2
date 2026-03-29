from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="news_articles")

    slug = models.SlugField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    intro = models.CharField(max_length=250, default="")
    body = models.TextField()

    tags = models.JSONField(default=list, blank=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})
