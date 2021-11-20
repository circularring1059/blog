from django.shortcuts import render

from django.http import HttpResponse

from .models import ArticlePost


def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = { 'articles': articles }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', locals())


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    return render(request, 'article/detail.html', locals())