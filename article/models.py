from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone


class ArticlePost(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    update = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=9)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

# class article_detail(models.Model):
#     article =




