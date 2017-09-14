from django.shortcuts import render
from .models import *
from hashlib import sha1
# Create your views here.
def login(request):
    return render(request,'tt_user/login.html')
def register(request):
    return render(request,'tt_user/register.html')

def registeron(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    uemail = post.get('email')
    user = UserInfo()
    user.uname = uname
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    sha_upwd=s1.hexdigest()
    user.upwd = sha_upwd
    user.uemail = uemail
    user.save()
    return render(request,'tt_user/register.html')