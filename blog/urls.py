from django.conf.urls import *
from blog.views import *
from django.conf import settings
urlpatterns=patterns('',url(r'^$',bloglist),
                        url(r'^page/(?P<page>\d+)$',homepage),
                        url(r'^(\d+)$',bloglist),
                        url(r'^(?P<index>\d+)/viewmode/(?P<viewmode>[\u4e00-\u9fa5\w+]+)$',bloglist),
                        url(r'^(?P<index>\d+)/page/(?P<page>\d+)$',bloglist),
                        url(r'index$',homepage),
                        url(r'gologin$',gologin),
                        url(r'goregister$',goregister),
                        url(r'register$',register),
                        url(r'login$',login),
                        url(r'(\d+)/logout$',logout),
                        url(r'^(\d+)/article/(\d+)$',blogdetail),
                        url(r'^(\d+)/article/(\d+)/submit$',blogcomment),
                        url(r'css/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[0],'show_indexes':True}),
                        url(r'pic/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[1],'show_indexes':True}),
                        url(r'js/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS[2],'show_indexes':True}),
                        url(r'(\d+)/category/([\u4e00-\u9fa5\w+]+)$',blogcategory),
                        url(r'(\d+)/category/([\u4e00-\u9fa5\w+]+)/page/(\d+)$',blogcategory),
                        url(r'(\d+)/create/submitblog$',createblog), 
                        url(r'^(\d+)/edit$',createpage),
                        url(r'^(\d+)/edit/(\d+)$',showeditblogpage),
                        url(r'(\d+)/categorymanage/addcategory$',addcategory),
                        url(r'(\d+)/categorymanage$',categorymanage),
                        url(r'(\d+)/categorymanage/edit$',categoryedit),
                        url(r'(\d+)/categorymanage/delete/([\u4e00-\u9fa5\w+]+)$',deletecategory),
                        url(r'(\d+)/articlemanage$',articlemanage),
                        url(r'(\d+)/articlemanage/delete/(\d+)$',deletearticle),
                        url(r'(\d+)/edit/submitblog/(\d+)$',doeditblog),


)
