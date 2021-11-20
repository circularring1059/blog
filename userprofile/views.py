from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .form import UserLoginForm, UserRegisterForm

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        # print(user_login_form)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            # user = authenticate(username=data.get("username"), password=data.get('password'))
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("article:article_list")
            else:
                # return HttpResponse("用户名或密码输入有误，请重新登入")
                msg = "用户名或密码不正确,请重新输入"
                # return redirect("userprofile:login", locals())
                return render(request, 'userprofile/login.html', locals())
        else:
            return HttpResponse("输入不合法")
    elif request.method == "GET":
        user_login_form = UserLoginForm
        return render(request, "userprofile/login.html", locals())
    else:
        return HttpResponse("request method is forbid")

def user_logout(request):
    logout(request)
    return redirect("article:article_list")


def user_register(request):
    if request.method == "POST":
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()

            #注册完成进行登入
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse('输入有误，请重新输入')
    elif request.method == "GET":
        # user_register_form = UserRegisterForm()
        # print(user_register_form)
        return render(request, "userprofile/register.html", locals())
    else:
        return HttpResponse("request method is forbid")


