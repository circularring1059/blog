from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth.models import User

from comment.models import Comment
from .forms import ArticlePostForm
from django.core.paginator import Paginator

from .models import ArticlePost

import markdown
def article_list(request):
    # # 取出所有博客文章
    # articles = ArticlePost.objects.all()
    # # 需要传递给模板（templates）的对象
    # context = { 'articles': articles }
    # # render函数：载入模板，并返回context对象
    # return render(request, 'article/list.html', locals())
    #分页
    #判断是否为文章搜索
    search = request.GET.get('search')
    if search:
        article_list = ArticlePost.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        article_list = ArticlePost.objects.all()
    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request, "article/list.html", locals())



def article_detail(request, id):
    #获取评论
    comments = Comment.objects.filter(article=id)
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
    extensions=[
        "markdown.extensions.extra",
        'markdown.extensions.codehilite'
    ])
    #浏览加一
    article.total_views += 1
    article.save(update_fields=['total_views'])
    return render(request, 'article/detail.html', locals())

#forms
def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            #先不commit,要加user
            new_article = article_post_form.save(commit=False)
            new_article.auth = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("提交有误，请重试")

    else:
        article_post_form = ArticlePostForm()

        return render(request, 'article/create.html', locals())


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    article = ArticlePost.objects.get(id=id)

    if request.user != article.auth:
        return HttpResponse("permission denied")

    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST.get("title")
            article.body = request.POST.get("body")
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse('表单有误，请重新填写')

    else:
        article_post_form = ArticlePostForm()
        return render(request, "article/update.html", locals())







