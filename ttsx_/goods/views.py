from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from tt_user.models import *
from tt_cart.models import *
from django.core.paginator import Paginator
from django.template import RequestContext, loader
import time
from django.db.models import Count

# Create your views here.



def index(request):
    #获取类型列表
    typelist = TypeInfo.objects.all()
    #获取商品列表

    #按type查找商品，返回结果的前4个
    fruitlist = typelist[0].goodsinfo_set.all()[0:4]
    seafoodlist = typelist[1].goodsinfo_set.all()[0:4]
    meetlist = typelist[2].goodsinfo_set.all()[0:4]
    egglist = typelist[3].goodsinfo_set.all()[0:4]
    vegetableslist = typelist[4].goodsinfo_set.all()[0:4]
    icelist = typelist[5].goodsinfo_set.all()[0:4]

    content = {'type':typelist,
               'fruit':fruitlist,
               'seafood':seafoodlist,
               'meet':meetlist,
               'egg':egglist,
               'vegetables':vegetableslist,
               'ice':icelist,
               }

    return render(request, 'goods/index.html', content)

def list1(request,pid,pidex,sort):
    #根据pid查找对应的商品类型
    type = TypeInfo.objects.get(id=pid)
    #判断 商品类型如果为大于6，则返回全部商品页面
    if int(pid) <= 6:
        # 新品推荐页面的两个商品
        newgoods = type.goodsinfo_set.order_by('id')[0:2]
        if int(sort) == 1:
            #默认商品展示排序直接返回全部商品
            goodslist = type.goodsinfo_set.all()
        elif int(sort) == 2:
            #返回按价格排序的商品
            goodslist = type.goodsinfo_set.order_by('-gprice')
        else:
            goodslist =type.goodsinfo_set.order_by('-gclick')
    else:
        #当请求为全部商品时
        newgoods = GoodsInfo.objects.order_by('-id')[0:2]
        goodslist = GoodsInfo.objects.order_by('-id')
    p = Paginator(goodslist, 10)
    #每页展示10个
    page = p.page(int(pidex))
    context ={'type':type,
              'new':newgoods,
              'page':page,
              'paginator':p,
              'sort':sort,
    }
    return render(request,'goods/list.html',context)

def detail(request,id):
    goods = GoodsInfo.objects.get(id=id)
    #根据id 查找对应商品
    typ = TypeInfo.objects.get(ttitle=goods.gtype)
    #查找到对应商品的类型
    newgoods = typ.goodsinfo_set.order_by('id')[0:2]
    #查找到对应类型的其中两个商品，用于页面的推荐商品展示
    goods.gclick +=1
    #打开页面时，该商品的点击量加1 （gclick）
    price=goods.gprice
    goods.save()
    #保存到数据库
    content = RequestContext(request,{'goods':goods,
               'new':newgoods,
               'type':typ,
               'price': price,
               })
    rep = render(request, 'goods/detail.html', content)

    #点开页面后，对应的商品id会被存入cookie
    rep.set_cookie(id,id)
    return rep

def info(request,key,numb,id):
    numb=int(numb)
    key=int(key)
    id=int(id)
    goods = GoodsInfo.objects.get(id=id)
    kucun = goods.gkucun
    print(type(id))
    if key>=1:
        if key==1:
            numb +=1
        else:
            numb = int(numb)

    elif key==0:
        numb -=1

    if numb >= kucun:
        numb = kucun
    if numb <= 1:
        numb = 1

    allprice = goods.gprice * numb

    content={'numb': numb,
            'price': allprice,
             }

    return JsonResponse({'data':content})


def json(request):
    uname = request.GET.get('n')
    userobject = UserInfo.objects.get(uname=uname)
    cartlist = CartInfo.objects.filter(user=userobject)
    id = request.GET.get('id')
    #商品
    goods = GoodsInfo.objects.get(id=id)

    count = len(cartlist)
    print()
    return JsonResponse({'data':count})