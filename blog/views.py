from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib import auth
from blog.models import *
from django.http import JsonResponse
from bs4 import BeautifulSoup
from blog.forms import RegisterForm
import os
from  cnblog  import settings
# Create your views here.


class Index(View):
    def get(self,request,*args,**kwargs):
        article_list = Article.objects.all()
        return render(request,"index.html",locals())


def get_valid_img(request):
    import random
    from PIL import Image
    from io import BytesIO
    from PIL import ImageDraw, ImageFont

    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    f = BytesIO()
    image = Image.new(mode="RGB", size=(120, 80), color=get_random_color())
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("kumo.ttf", size=36)
    temp = []
    for i in range(5):
        random_char = random.choice(
            [str(random.randint(0, 9)), chr(random.randint(65, 90)), chr(random.randint(97, 122))])
        draw.text((i * 24, 26), random_char, get_random_color(), font=font)
        temp.append(random_char)
    image.save(f, "png")
    data = f.getvalue()
    request.session["random_code_str"] = "".join(temp)
    print(request.session.get("random_code_str"))
    return HttpResponse(data)


class Login(View):

    def get(self,request,*args,**kwargs):
        return render(request,"login.html")

    def post(self, request, *args, **kwargs):
        response = {"status":True,"msg":None}
        validcode = request.POST.get("validcode")
        if validcode.upper() != request.session.get("random_code_str").upper():
            response["status"] = False
            response["msg"] = "验证码错误"
            return JsonResponse(response)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return JsonResponse(response)
        else:
            response["status"] = False
            response["msg"] = "用户名或密码错误!"
            return JsonResponse(response)


class Logout(View):

    def get(self,request,*args,**kwargs):
        auth.logout(request)
        return redirect("/cnblog.com/")


# 个人站点
class Homesite(View):

    def get(self,request,*args,**kwargs):
        username = kwargs["username"]
        user = UserInfo.objects.filter(username=username).first()
        if user:
            if not kwargs.get("condition"):
                article_list = Article.objects.filter(user=user)
            else:
                condition = kwargs.get("condition")
                parma = kwargs.get("param")
                if condition == "category":
                    article_list = Article.objects.filter(user=user).filter(category__title=parma)
                elif condition == "tag":
                    article_list = Article.objects.filter(user=user).filter(tags__title=parma)
                else:
                    article_list = Article.objects.filter(user=user).filter(create_time__startswith=parma)
            return render(request,"homesite.html",locals())
        else:
            return render(request,"not_found.html")


class Article_detail(View):

    def get(self,request,*args,**kwargs):
        article_id = int(kwargs["article_id"])
        article_obj = Article.objects.filter(pk=article_id).first()
        user = UserInfo.objects.filter(username=kwargs.get("username")).first()
        comment_list = Comment.objects.filter(article_id=article_id)
        if not article_obj:
            return render(request,"not_found.html")
        return render(request,"article.html",locals())


class Up_down(View):

    def get(self,request,*args,**kwargs):
        return HttpResponse("ok")

    def post(self, request, *args, **kwargs):
        import json
        from django.http import JsonResponse
        article_id = request.POST.get("article_id")
        is_up = json.loads(request.POST.get("is_up"))
        response = {"status":True,"msg":None}

        is_upobj = ArticleUpDown.objects.filter(user=request.user,article_id=article_id).first()
        if is_upobj:
            response["status"] = False
            if is_upobj.is_up:
                response["msg"]  = "您已经推荐过！"
            else:
                response["msg"] = "您已经反对过！"
            return JsonResponse(response)
        else:
            from django.db.models import F
            from django.db import transaction
            #  将创建点赞与踩灭记录和对应数量的增加合并为一个事物，使其同进同退
            with transaction.atomic():
                ArticleUpDown.objects.create(user=request.user,is_up=is_up,article_id=article_id)
                if is_up:
                    Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
                else:
                    Article.objects.filter(pk=article_id).update(down_count=F("down_count")+1)
            return JsonResponse(response)


class Sub_comment(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse("ok")

    def post(self,request,*args,**kwargs):
        article_id = request.POST.get("article_id")
        comment = request.POST.get("comment")
        parent_id = request.POST.get("parent_id")
        Comment.objects.create(user=request.user,article_id=article_id,content=comment,parent_comment_id=parent_id)
        return HttpResponse("ok")


class Backend(View):
    def get(self,request,*args,**kwargs):
        print("BBB",request.user.username)
        if not request.user.username:
            return redirect("/cnblog.com/login/")
        article_list = Article.objects.filter(user=request.user)
        return render(request,"backend.html",locals())

    def post(self,request,*args,**kwargs):
        return HttpResponse("ok")


class Addarticle(View):
    def get(self,request,*args,**kwargs):
        article_list = Article.objects.filter(user=request.user)
        return render(request,"addarticle.html",locals())

    def post(self,request,*args,**kwargs):
        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.user
        soup = BeautifulSoup(content, "html.parser")
        # 过滤非法标签
        for tag in soup.find_all():
            if tag.name in ["script", ]:
                tag.decompose()
        # 获取文章摘要内容
        desc = soup.text[0:150]
        Article.objects.create(title=title, content=str(soup), user=user, desc=desc)
        return redirect("/backend/")


class Editor(View):
    def get(self,request,*args,**kwargs):
        article_id = kwargs.get("article_id")
        article_obj = Article.objects.filter(pk=article_id).first()
        return render(request,"editarticle.html",locals())

    def post(self,request,*args,**kwargs):
        article_id = kwargs.get("article_id")
        title = request.POST.get("title")
        content = request.POST.get("content")
        user = request.user
        soup = BeautifulSoup(content, "html.parser")
        # 过滤非法标签
        for tag in soup.find_all():
            if tag.name in ["script", ]:
                tag.decompose()
        # 获取文章摘要内容
        desc = soup.text[0:150]
        Article.objects.filter(pk=article_id).update(title=title,desc=desc,user=user,content=str(soup))
        return redirect("/backend/")


class Delete(View):
    def get(self,request):
        print("搜索功能")
        print("购物车功能")
        print("添加在线直播功能")
        return HttpResponse("ok")


# 注册视图
class Register(View):
    def get(self,request,*args,**kwargs):
        register_form = RegisterForm()
        return render(request,"register.html",locals())

    def post(self,request,*args,**kwargs):
        register_form = RegisterForm(request.POST)
        reg_response = {"user": None, "error_msg": None}
        if register_form.is_valid():
            user = register_form.cleaned_data.get("user")
            pwd = register_form.cleaned_data.get("pwd")
            email = register_form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")  # 图片对象
            user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar_obj)
            reg_response["user"] = user_obj.username
        else:
            reg_response["error_msg"] = register_form.errors
        import json
        return HttpResponse(json.dumps(reg_response))


# 富文本编辑器图片上传
class Up_load(View):
    def post(self,request,*args,**kwargs):
        print(request.FILES)
        obj = request.FILES.get("upload_img")
        name = obj.name
        path = os.path.join(settings.BASE_DIR, "static", "upload", name)
        with open(path, "wb") as f:
            for line in obj:
                f.write(line)
        import json
        res = {
            "error": 0,
            "url": "/static/upload/" + name
        }
        return HttpResponse(json.dumps(res))