from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse,HttpResponse
import datetime
from hashlib import sha1
from django.core.mail import send_mail
from django.conf import settings
from .judge import *

# Create your views here.
# 注册页面
def register(request):

    return render(request,'tt_user/register.html')

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

    return render(request,'tt_user/login.html')


# 登录处理
def login_handle(request):
    dict = request.POST
    uname = dict.get('username')
    upwd = dict.get('pwd')
    remember = dict.get('remember')

    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd_sha = s1.hexdigest()
    user = UserInfo.users.get(uname = uname)
    if user.upwd == upwd_sha:
        request.session['uid'] = user.id
        request.session['uname'] = user.uname
        enter = redirect(request.session.get('lastpath ','/user/user_center_info'))
        if remember == 'on':
            enter.set_cookie('uname',value=uname,expires= datetime.date.today()+ datetime.timedelta(1))
        return enter
    else:
        return HttpResponse('密码错误,登录失败,请重新<a href="/user/login/">登录</a>')

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