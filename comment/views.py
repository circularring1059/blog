from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from article.models import ArticlePost

from .forms import CommentForm

# @login_required(login_url="/userprofile/login/")
# def post_comment(request, article_id):
#     article = get_object_or_404(ArticlePost, id=article_id)
#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.
#             new_comment.article = article
#             new_comment.user = request.user
#             new_comment.save()
#             return redirect(article)
#         else:
#             return HttpResponse("内容非法")
#
#     else:
#         return HttpResponse("request method forbid need POST")

# 文章评论
from .models import Comment


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            comments = Comment.objects.filter(article=article_id)
            # return redirect(article)
            return render(request, 'article/detail.html', locals())

        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")