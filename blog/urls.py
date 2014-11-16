from django.conf.urls import *
from blog.views import *
from django.conf import settings
urlpatterns=patterns('',url(r'^$',homepage),
                        url(r'^(\d+)$',archive),
                        url(r'index$',homepage),
                        url(r'gologin$',gologin),
                        url(r'goregister$',goregister),
                        url(r'register$',register),
                        url(r'login$',login),
                        url(r'^article/(\d+)$',blogdetail),
                        url(r'css/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[0],'show_indexes':True}),
                        url(r'pic/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[1],'show_indexes':True}),
                        url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[2],'show_indexes':True}),
                        url(r'category/([\u4e00-\u9fa5\w+]+)$',blogcategory),
                        url(r'create/submitblog$',createblog), 
                        url(r'^edit$',createpage),
                        url(r'^edit/(\d+)$',showeditblogpage),
                        url(r'categorymanage/addcategory$',addcategory),
                        url(r'categorymanage$',categorymanage),
                        url(r'categorymanage/delete/([\u4e00-\u9fa5\w+]+)$',deletecategory),
                        url(r'articlemanage$',articlemanage),
                        url(r'articlemanage/delete/(\d+)$',deletearticle),
                        url(r'edit/submitblog/(\d+)$',doeditblog),


)
