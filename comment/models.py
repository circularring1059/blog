from django.db import models

from django.contrib.auth.models import User
from article.models import ArticlePost
from mptt.models import MPTTModel, TreeForeignKey

from ckeditor.fields import RichTextField

# class Comment(models.Model):
#     article = models.ForeignKey(
#         ArticlePost,
#         on_delete=models.CASCADE,
#         related_name='comment'
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comment'
#     )
#     body= models.TextField()
#     created = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ("created",)
#
#     def __str__(self):
#         return self.body[:20]

class MultipyComment(MPTTModel):
    # body = models.TextField()
    body = RichTextField()
    created = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replyers",
    )

    class MPTTMeta:
        order_insertion_by = ["created"]

    def __str__(self):
        return self.body[:20]