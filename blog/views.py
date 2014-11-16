from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import BlogPost,BlogTable1, BlogCategory,User
import datetime

def login(request):
    if "userID" in request.session:
        return HttpResponseRedirect('/blog/'+str(request.session['userID']))
    else: 
    	username=request.POST['Name']
        userpassword=request.POST['Password']
        authuser=User.objects.get(name=username,password=userpassword)
        cid=authuser.id 
        if authuser is not None:
            request.session['userID']=cid
            request.session['userName']=username 
            return HttpResponseRedirect('/blog/'+str(cid))



def register(request):  
    name=request.POST['Name']
    password=request.POST['Password'] 
    user=User(name=name,password=password)
    user.save()
    post=BlogTable1.objects.all()
    category=BlogCategory.objects.all()
    categorynum=category.count()
    t=loader.get_template("bloglist.html")
    c=RequestContext(request,{'posts':post,'category':category})
    return HttpResponse(t.render(c))
  
   # return render_to_response('register.html', {'errors': errors},context_instance=RequestContext(request)) 
def homepage(request):
    blogs=BlogTable1.objects.all()
    return render_to_response('index.html',{'blogs':blogs},context_instance=RequestContext(request)) 

def gologin(request):
    return render_to_response('login.html',context_instance=RequestContext(request))

def goregister(request):
    return render_to_response('register.html',context_instance=RequestContext(request))


def archive(request,index):
    post=BlogTable1.objects.filter(userID=index)
    category=BlogCategory.objects.filter(userID=index)
    username=User.objects.get(id=index).name
    categorynum=category.count()
    t=loader.get_template("bloglist.html")
    if 'userID' in request.session:
        if str(request.session['userID'])==index:
            c=Context({'posts':post,'username':username,'category':category,'logined':'true'})
            return HttpResponse(t.render(c))
        else:
            c=Context({'posts':post,'username':username,'category':category})
            return HttpResponse(t.render(c))
    else:
        c=Context({'posts':post,'username':username,'category':category})
        return HttpResponse(t.render(c))

def blogdetail(request,index):
    post=BlogTable1.objects.get(id=index)
    categorys=BlogCategory.objects.all()
    t=loader.get_template("details.html")
    c=Context({'post':post,'categorys':categorys})
    return HttpResponse(t.render(c))

def blogcategory(request,string):
    post=BlogTable1.objects.filter(category=string)
    category=BlogCategory.objects.all()
    t=loader.get_template("category.html")
    c=Context({'posts':post,'category':category})
    return HttpResponse(t.render(c))

def createpage(request):
    category=BlogCategory.objects.all()
    categoryblock=RequestContext(request,{'categorys':category})
    t=loader.get_template("createblog.html")
    return HttpResponse(t.render(categoryblock))
   # return render_to_response('editblog.html',categoryblock,context_instance=RequestContext(request))

def createblog(request):
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

def showeditblogpage(request,index):
    article=BlogTable1.objects.get(id=index)
    categorys=BlogCategory.objects.all()
    categoryblock=RequestContext(request,{'article':article,'categorys':categorys})
    t=loader.get_template("editblog.html")
    return HttpResponse(t.render(categoryblock))

def doeditblog(request,index):
    originarticle=BlogTable1.objects.get(id=index)
    if originarticle.category.name==request.POST['blogcategory']:
       time=datetime.datetime.now()
       BlogTable1.objects.filter(id=index).update(title=request.POST['blogtitle'],body=request.POST['blogcontent'],timestamp=time)
    else:
       changeedcag=BlogCategory.objects.get(name=originarticle.category.name)
       changeedcag.num-=1
       changeedcag.save()
       updatecag=BlogCategory.objects.get(name=request.POST['blogcategory'])
       updatecag.num+=1
       updatecag.save()
       time=datetime.datetime.now()
       BlogTable1.objects.filter(id=index).update(title=request.POST['blogtitle'],body=request.POST['blogcontent'],category=updatecag,timestamp=time)
    post=BlogTable1.objects.all()
    category=BlogCategory.objects.all()
    categorynum=category.count()
    t=loader.get_template("bloglist.html")
    c=Context({'posts':post,'category':category})
    return HttpResponse(t.render(c))

     
 

