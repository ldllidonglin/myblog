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
            request.session['userName']=username
            request.session['userID']=cid 
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
    if 'userName' in request.session:
        return render_to_response('index.html',{'blogs':blogs,'userName':request.session['userName'],'userID':request.session['userID']},context_instance=RequestContext(request)) 
    else:
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
            c=Context({'posts':post,'userName':username,'userID':request.session['userID'],'category':category,'logined':'true'})
            return HttpResponse(t.render(c))
        else:
            c=Context({'posts':post,'userName':username,'category':category,'userID':index})
            return HttpResponse(t.render(c))
    else:
        c=Context({'posts':post,'userName':username,'category':category,'userID':index})
        return HttpResponse(t.render(c))

def blogdetail(request,index1,index):
    post=BlogTable1.objects.get(id=index,userID=index1)
    categorys=BlogCategory.objects.filter(userID=index1)
    if post is not None:
       t=loader.get_template("details.html")
       c=Context({'post':post,'categorys':categorys,'userID':post.userID,'userName':post.userName})
       return HttpResponse(t.render(c))
    else:
       blogs=BlogTable1.objects.all()
       return render_to_response('index.html',{'blogs':blogs},context_instance=RequestContext(request))

def blogcategory(request,index,string):
       post=BlogTable1.objects.filter(userID=index,category=string)
       currentuser=User.objects.get(id=index);
       username=currentuser.name 
       category=BlogCategory.objects.filter(userID=index)
       t=loader.get_template("category.html")
       c=Context({'posts':post,'category':category,'userName':username,'userID':index})
       return HttpResponse(t.render(c))

def createpage(request,index):
    category=BlogCategory.objects.filter(userID=index)
    currentuser=User.objects.get(id=index)
    if currentuser is not None:
       categoryblock=RequestContext(request,{'categorys':category,'userID':currentuser.id,'userName':currentuser.name})
       t=loader.get_template("createblog.html")
       return HttpResponse(t.render(categoryblock))
   # return render_to_response('editblog.html',categoryblock,context_instance=RequestContext(request))

def createblog(request,index):
    c=BlogCategory.objects.get(name=request.POST['blogcategory'])
    c.num=c.num+1
    c.save()
    time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    currentuser=User.objects.get(id=index);
    username=currentuser.name;
    userid=currentuser.id;
    p=BlogTable1(userID=index,userName=username,title=request.POST['blogtitle'],body=request.POST['blogcontent'],category=c,timestamp=time) 
    p.save()
    post=BlogTable1.objects.get(id=p.id)
    categorys=BlogCategory.objects.filter(userID=userid)
    t=loader.get_template("details.html")
    c=Context({'post':post,'categorys':categorys,'userName':username,'userID':userid})
    index=bytes(index)
    bid=str(p.id)
    reurl="/blog/"+index+"/article/"+bid
    return HttpResponseRedirect(reurl)

@csrf_protect
def addcategory(request,uid):
    if uid==str(request.session['userID']):
       cate=BlogCategory(name=request.POST['addcagname'],userID=request.session['userID'])
       cate.save()
      # c=RequestContext(request,{'categorys':categorys,'userID':request.session['userID']})
       return HttpResponseRedirect("/blog/"+uid+"/categorymanage")

def articlemanage(request,index):
    if index==str(request.session['userID']):
       articles=BlogTable1.objects.filter(userID=request.session['userID'])
       t=loader.get_template("articlemanage.html")
       c=Context({'articles':articles,'userID':request.session['userID']})
       return HttpResponse(t.render(c))
    else:
       return HttpResponseRedirect("/blog")

def categorymanage(request,index):
    if index==str(request.session['userID']):
       categorys=BlogCategory.objects.filter(userID=request.session['userID']);
       t=loader.get_template("categorymanage.html")
       c=RequestContext(request,{'categorys':categorys,'userID':index})
       return HttpResponse(t.render(c)) 
    else:
       return HttpResponseRedirect("/blog/"+index)

def deletecategory(request,index,string):
    if index==str(request.session['userID']):
       categorys=BlogCategory.objects.get(name=string,userID=index)
       categorys.delete()
       categorys=BlogCategory.objects.all();
       t=loader.get_template("categorymanage.html")
       c=Context({'categorys':categorys,'userID':index})
       return HttpResponse(t.render(c))
    else:
       return HttpResponseRedirect("/blog")

def deletearticle(request,uid,index):
    if uid==str(request.session['userID']):
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
    else:
       return HttpResponseRedirect("/blog")

def showeditblogpage(request,uid,index):
    if uid==str(request.session['userID']):
       article=BlogTable1.objects.get(userID=uid,id=index)
       categorys=BlogCategory.objects.all()
       categoryblock=RequestContext(request,{'article':article,'categorys':categorys,'userID':uid})
       t=loader.get_template("editblog.html")
       return HttpResponse(t.render(categoryblock))
    else:
       return HttpResponseRedirect("/blog") 

def doeditblog(request,uid,index):
    if uid==str(request.session['userID']):
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
       return HttpResponseRedirect("/blog/"+uid+"/article/"+index)
    else:
        return HttpResponseRedirect("/blog")

     
 

