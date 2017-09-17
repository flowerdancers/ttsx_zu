from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse,HttpResponse
import datetime
from hashlib import sha1
from django.core.mail import send_mail
from django.conf import settings
from .judge import *
from PIL import Image, ImageDraw, ImageFont

# Create your views here.
# 注册页面
def register(request):
    context = {'title':'注册'}
    return render(request,'tt_user/register.html',context)

# 重名判断
def has_user(request):
    has = False
    reg_name = request.GET.get('uname')
    uname = UserInfo.users.filter(uname__exact=reg_name)
    if uname:
        has = True
    return JsonResponse({'reg_name':has})

# 注册用户
def register_handle(request):
    dict = request.POST

    uname = dict.get('user_name')
    upwd = dict.get('pwd')
    uemail = dict.get('email')

    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd_sha = s1.hexdigest()

    user = UserInfo.users.create(uname,upwd_sha,uemail)
    user.save()

    msg = '<a href="http://127.0.0.1:8000/active%s/">点击激活</a>'%(user.id)
    send_mail('天天生鲜用户激活',"",settings.EMAIL_FROM,['python01zt@163.com'],html_message=msg)
    return HttpResponse('用户注册成功,请进入邮箱激活')

# 激活
def active(request,uid):
    user = UserInfo.users.get(id = uid)
    user.isActive = True
    user.save()
    return HttpResponse('激活成功,点击<a href="/user/login/">登录</a>跳转到登录界面')

# 登录
def login(request):
    uname = request.COOKIES.get('user_name', '')
    context = {'title': '登录', 'uname': uname}
    return render(request, 'tt_user/login.html', context)

# 登录处理
def login_handle(request):
    # 判断请求方式
    if request.method == 'GET':
        return redirect('/user/login')
    dict = request.POST
    uname = dict.get('username')
    upwd = dict.get('pwd')
    remember = dict.get('remember','0')
    yzm = dict.get('yzm')
    context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'uname_error': 0, 'upwd_error': 0}


    user = UserInfo.users.filter(uname = uname)
    # 判断用户是否存在
    if user:
        upwd_db = user[0].upwd
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        upwd_sha = s1.hexdigest()
        # 密码判断
        if upwd_db == upwd_sha:
            # 判断是否激活
            if user[0].isActive:
                # 登录成功
                response = redirect(request.session.get('url_path', '/'))
                # 记住用户名
                request.session['uid'] = user[0].id
                request.session['uname'] = uname
                if remember == '1':
                    response.set_cookie('user_name',uname,expires=60*60)
                else:
                    response.set_cookie('user_name','',expires=-1)
                return response
            else:
                return HttpResponse('账户还未激活，请先到邮箱中激活账户')
        else:
            context['upwd_error'] = 1
            return render(request,'tt_user/login.html',context)
    else:
        context['uname_error'] = 1
        retur

# 验证码
def verify_code(request):
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
            20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    from io import BytesIO
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

# 用户中心
@judge
def user_center_info(request):
    context = {'title':'用户中心'}
    list = UserAddressInfo.objects.filter(user_id = request.session.get('uid'))
    if len(list) == 1:
        uname = list[0].uname
        uphone = list[0].uphone
        ucode = list[0].ucode
        uaddr_detail = list[0].uaddr_detail
        context = {'uname':uname,'uphone':uphone,'ucode':ucode,'uaddr_detail':uaddr_detail}
    return render(request, 'tt_user/user_center_info.html', context)

def user_center_order(request):
    return render(request,'tt_user/user_center_order.html')

# 收货地址处理
def user_site(request):
    dict = request.POST
    recv_name = dict.get('recv_name')
    addr_detail = dict.get('addr_detail')
    ucode = dict.get('ucode')
    uphone = dict.get('phone')
    recv_user = UserAddressInfo()
    recv_user.uname = recv_name
    recv_user.uaddr_detail = addr_detail
    recv_user.ucode = ucode
    recv_user.uphone = uphone

    recv_user.user_id = request.session.get('uid')
    recv_user.save()
    context = {'addr_detail': addr_detail, 'recv_name': recv_name, 'uphone': uphone}
    # context['title'] = '地址'
    return render(request,'tt_user/user_center_site.html',context)

# 收货地址页面
@judge
def user_center_site(request):
    context = {'title': '收货地址'}
    recv = UserAddressInfo.objects.filter(user_id=request.session.get('uid'))
    context['addr'] = recv[0].uaddr_detail
    context['recv'] = recv[0].uname
    context['phone'] = recv[0].uphone
    return render(request,'tt_user/user_center_site.html',context)

def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def close(request):
    request.session.flush()
    return

def index(request):
    return render(request,'tt_user/index.html')

def cart(request):
    return render(request,'tt_user/cart.html')