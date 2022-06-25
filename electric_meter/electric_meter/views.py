from django.contrib import messages
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from .infer import *
from .settings import BASE_DIR
import os
import time
import datetime
import pandas
from dbmodel.models import Info
from django.contrib import auth
from django.contrib.auth.models import User


def recognition(request):
    return render(request, "image_upload.html")


def index(request):
    return render(request, "index.html", {})


def pic_upload(request):
    submit_pic = request.FILES.get('pic')
    pic_suffix = submit_pic.name.split(".")[-1]  # 获取后缀
    pic_path = os.path.join(str(time.time()) + "." + pic_suffix)  # 构造文件路径
    with open(os.path.join(BASE_DIR, "upload", pic_path), "wb") as f:
        for line in submit_pic:
            f.write(line)
    img_path = os.path.join(BASE_DIR, "upload", pic_path)
    try:
        result = electric_meter(img_path)
    except:
        messages.error(request, '您上传的文件不是合法的图片文件')
        return HttpResponseRedirect('/recognition')

    context = {}
    context["upload_states"] = "上传成功！%s" % result
    context["total_path"] = os.path.join(pic_path)
    result_list = []
    for i in range(len(result)):
        result_list.append(result[i][-1][0])

    try:
        result1 = result_list[0]
    except:
        result1 = ''
    try:
        result2 = result_list[1]
    except:
        result2 = ''
    context["result1"] = result1
    context["result2"] = result2
    context["result_list"] = result_list
    for i in result_list:
        if len(i) >= 7:
            context["result2"] = i
    return render(request, 'info_upload.html', context)


def info_upload(request):
    number = request.POST["num"]
    info = request.POST["info"]
    path = request.POST["path"]
    upload_time = os.path.basename(path)[:os.path.basename(path).rfind(".")]
    upload_time = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime(eval(upload_time)))
    db_obj = Info(number=number, info=info, image=path,upload_time=upload_time)
    db_obj.save()
    messages.error(request, "信息上传成功！")
    return HttpResponseRedirect("/recognition")


def info_list(request):
    infos = Info.objects.all()
    info_view = []
    for info in infos:
        info_view.append([info.upload_time, info.number, info.info, info.image])
    return render(request, "info_list.html", {"infos": info_view})


def to_excel(request):
    try:
        start = datetime.datetime.strptime(request.POST["start"], "%Y-%m-%dT%H:%M")
        end = datetime.datetime.strptime(request.POST["end"], "%Y-%m-%dT%H:%M")
        result = []
        for info in Info.objects.all():
            if start <= info.upload_time.replace(tzinfo=None) <= end:
                result.append([info.upload_time, info.number, info.info, info.image])
    except:
        result = []
        for info in Info.objects.all():
            result.append([info.upload_time.replace(tzinfo=None), info.number, info.info, info.image])
    df = pandas.DataFrame(result)
    df.columns = ['上传时间', '表盘读数', '备注', '图像路径']
    xls_name = os.path.join(BASE_DIR, "static", "temp_xls", "%s.xlsx" % str(time.time()))
    df.to_excel(xls_name, sheet_name="电表数据导出")
    response = FileResponse(open(xls_name, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(xls_name)
    return response


def user_view(request):
    try:
        context = {'info': request.GET['message']}
    except:
        context = {'info': "请先登录!"}
    return render(request, "user.html", context)


def user_oper(request):
    username = request.POST['username']
    password = request.POST['password']
    operat = request.POST['operat']
    if operat == "login":
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # Redirect to a success page.
            messages.error(request, "登陆成功！")
            return HttpResponseRedirect('index')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "用户名或密码错误！")
            return HttpResponseRedirect('user?message=用户名或密码错误！')
    elif operat == "register":
        try:
            user = User.objects.create_user(username=username, password=password)
        except:
            messages.error(request, "用户名已存在！")
            return HttpResponseRedirect('user?message=用户名已存在！')
        return HttpResponseRedirect('user?message=注册成功，请登陆！')


def logout_view(request):
    auth.logout(request)
    messages.error(request, "用户已登出！")
    return HttpResponseRedirect('index')