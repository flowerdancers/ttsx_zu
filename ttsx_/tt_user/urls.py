#!----/usr/bin/env ipython3---
from django.conf.urls import url
from . import views
urlpatterns = [
    url('^register/$',views.register),
    url('^register_handle/$',views.register_handle),
    url('^has_user/$',views.has_user),
    url(r'^active(\d+)/$',views.active),

    url('^login/$',views.login),
    url('^login_handle/$',views.login_handle),
    url('^logout/$',views.logout),
    url('^close/$',views.close),

    url('^user_center_info/$',views.user_center_info),
    url('^user_center_order/$',views.user_center_order),
    url('^user_site/$',views.user_site),
    url('^user_center_site/$',views.user_center_site),
    url('^index/$',views.index),
    url('^cart/$',views.cart),


]