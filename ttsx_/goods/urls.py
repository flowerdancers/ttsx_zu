from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$',views.index),
    url(r'index.html',views.index),
    # url(r'list/$',views.list),
    url(r'list(\d+)_(\d+)_(\d+)/',views.list1),
    url(r'detail(\d+)/',views.detail),
    url(r'info(\d+)_(\d+)_(\d+)/',views.info),
    url(r'json/',views.json),
    ]