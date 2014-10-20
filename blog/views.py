from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import loader,Context,RequestContext
from django.http import HttpResponse
from blog.models import BlogPost,BlogTable1, BlogCategory
import datetime
def archive(request):
    post=BlogTable1.objects.all()
    category=BlogCategory.objects.all()
    categorynum=category.count()
    t=loader.get_template("bloglist.html")
    c=Context({'posts':post,'category':category})
    return HttpResponse(t.render(c))

def blogdetail(request,index):
    post=BlogTable1.objects.get(id=index)
    t=loader.get_template("details.html")
    c=Context({'post':post})
    return HttpResponse(t.render(c))

def blogcategory(request,string):
    post=BlogTable1.objects.filter(category=string)
    category=BlogCategory.objects.all()
    t=loader.get_template("category.html")
    c=Context({'posts':post,'category':category})
    return HttpResponse(t.render(c))

def editpage(request):
    category=BlogCategory.objects.all()
    categoryblock=RequestContext(request,{'categorys':category})
    t=loader.get_template("editblog.html")
    return HttpResponse(t.render(categoryblock))
   # return render_to_response('editblog.html',categoryblock,context_instance=RequestContext(request))

def editblog(request):
    c=BlogCategory.objects.get(name=request.POST['blogcategory'])
    c.num=c.num+1
    c.save()
    time=datetime.datetime.now()
    p=BlogTable1(title=request.POST['blogtitle'],body=request.POST['blogcontent'],category=c,timestamp=time) 
    p.save()
    post=BlogTable1.objects.get(id=p.id)
    t=loader.get_template("details.html")
    c=Context({'post':post})
    return HttpResponse(t.render(c))

@csrf_protect
def addcategory(request):
    cate=BlogCategory(name=request.POST['addcagname'])
    cate.save()
    categorys=BlogCategory.objects.all();
    t=loader.get_template("categorymanage.html")
    c=Context({'categorys':categorys})
    return HttpResponse(t.render(c))

def articlemanage(request):
    articles=BlogTable1.objects.all()
    t=loader.get_template("articlemanage.html")
    c=Context({'articles':articles})
    return HttpResponse(t.render(c))

def categorymanage(request):
    categorys=BlogCategory.objects.all();
    t=loader.get_template("categorymanage.html")
    c=RequestContext(request,{'categorys':categorys})
    return HttpResponse(t.render(c)) 

def deletecategory(request,index):
    categorys=BlogCategory.objects.get(name=index)
    categorys.delete()
    categorys=BlogCategory.objects.all();
    t=loader.get_template("categorymanage.html")
    c=Context({'categorys':categorys})
    return HttpResponse(t.render(c))

def deletearticle(request,index):
    article=BlogTable1.objects.get(id=index)
    article.delete()
    category=article.category
    dcategory=BlogCategory.objects.get(name=category.name)
    dcategory.num=dcategory.num-1
    dcategory.save()
    articles=BlogTable1.objects.all()
    t=loader.get_template("articlemanage.html")
    c=Context({'articles':articles})
    return HttpResponse(t.render(c))

