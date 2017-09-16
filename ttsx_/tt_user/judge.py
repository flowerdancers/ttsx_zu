#!----/usr/bin/env ipython3---
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def judge(func):
    def login_fun(request,*args,**kwargs):
        if request.session.get('uid'):
            return func(request,*args,**kwargs)
        else:
            load = HttpResponseRedirect('/user/login/')
            load.set_cookie('url',request.get_full_path())
            return load
    return login_fun