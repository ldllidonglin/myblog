#coding=utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from blog.models import BlogPost,BlogTable1, BlogCategory,User
import datetime,math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def login(request):
    username=request.POST['Name']
    userpassword=request.POST['Password']
    authuser=User.objects.get(name=username,password=userpassword)
    cid=authuser.id 
    if authuser is not None:
       request.session['userName']=username
       request.session['userID']=cid 
       return HttpResponseRedirect('/blog')

def logout(request,uid):
    authuser=User.objects.get(id=uid)
    if authuser is not None:
       del request.session["userName"]
       del request.session["userID"]
    return HttpResponseRedirect('/blog')

def register(request):  
    name=request.POST['Name']
    password=request.POST['Password'] 
    user=User(name=name,password=password)
    user.save()
    #categorynum=category.count()
    #t=loader.get_template("bloglist.html")
    #c=RequestContext(request,{'posts':post,'category':category})
    return HttpResponseRedirect("/blog/"+str(user.id))
  
   # return render_to_response('register.html', {'errors': errors},context_instance=RequestContext(request)) 
def homepage(request,page="1"):
    page=int(page)
    totalblognum=BlogTable1.objects.all().count()
    cpage=Page(totalblognum,'10','5',page,'/blog')
    pagedom=cpage.createdom()
    blogs=BlogTable1.objects.all()[cpage.startIndex:cpage.endIndex]
    if 'userName' in request.session:
        loginedname=request.session['userName']
        logineduser=User.objects.get(name=loginedname)
        return render_to_response('index.html',{'blogs':blogs,'pagedom':pagedom,'logineduser':logineduser,'userName':request.session['userName'],'userID':request.session['userID']},context_instance=RequestContext(request))
    else:
        return render_to_response('index.html',{'blogs':blogs,'pagedom':pagedom},context_instance=RequestContext(request)) 

def gologin(request):
    return render_to_response('login.html',context_instance=RequestContext(request))

def goregister(request):
    return render_to_response('register.html',context_instance=RequestContext(request))


def bloglist(request,index,page="1"):
    totalblognum=BlogTable1.objects.filter(userID=index).count()
    url='/blog/'+str(index)
    cpage=Page(totalblognum,'10','5',int(page),url)
    pagedom=cpage.createdom()
    bloglists=BlogTable1.objects.filter(userID=index)[cpage.startIndex:cpage.endIndex]
    category=BlogCategory.objects.filter(userID=index)
    username=User.objects.get(id=index).name
    categorynum=category.count()
    t=loader.get_template("bloglist.html")
    if 'userID' in request.session:
        loginedname=request.session['userName']
        logineduser=User.objects.get(name=loginedname)
        if str(request.session['userID'])==index:
            c=Context({'bloglists':bloglists,'pagedom':pagedom,'userName':username,'userID':request.session['userID'],'category':category,'admin':'true','logineduser':logineduser})
            return HttpResponse(t.render(c))
        else:
            c=Context({'bloglists':bloglists,'pagedom':pagedom,'userName':username,'category':category,'userID':index,'logineduser':logineduser})
            return HttpResponse(t.render(c))
    else:
        c=Context({'bloglists':bloglists,'pagedom':pagedom,'userName':username,'category':category,'userID':index})
        return HttpResponse(t.render(c))

def blogdetail(request,index1,index):
    post=BlogTable1.objects.get(id=index,userID=index1)
    categorys=BlogCategory.objects.filter(userID=index1)
    if post is not None:
       t=loader.get_template("details.html")
       if 'userID' in request.session:
           logineduser=User.objects.get(id=request.session['userID'])
           if index1==str(request.session['userID']):
              c=Context({'post':post,'categorys':categorys,'userID':post.userID,'userName':post.userName,'logineduser':logineduser,'admin':'true'})
              return HttpResponse(t.render(c))
           else:
              c=Context({'post':post,'categorys':categorys,'userID':post.userID,'userName':post.userName,'logineduser':logineduser})
              return HttpResponse(t.render(c))
       else:
            c=Context({'post':post,'categorys':categorys,'userID':post.userID,'userName':post.userName})
            return HttpResponse(t.render(c))
    else:
       blogs=BlogTable1.objects.all()
       return render_to_response('index.html',{'blogs':blogs},context_instance=RequestContext(request))

def blogcategory(request,index,string,page='1'):
    totalblognum=BlogTable1.objects.filter(userID=index,category=string).count()
    url='/blog/'+str(index)+'/category/'+string
    cpage=Page(totalblognum,'10','5',int(page),url)
    pagedom=cpage.createdom()
    post=BlogTable1.objects.filter(userID=index,category=string)[cpage.startIndex:cpage.endIndex]
    currentuser=User.objects.get(id=index);
    username=currentuser.name 
    category=BlogCategory.objects.filter(userID=index)
    t=loader.get_template("category.html")
    if 'userID' in request.session:
        logineduser=User.objects.get(id=request.session['userID'])
        if index==str(request.session['userID']):
            c=Context({'posts':post,'category':category,'pagedom':pagedom,'userName':username,'userID':index,'admin':'true','logineduser':logineduser})
            return HttpResponse(t.render(c)) 
        else:
            c=Context({'posts':post,'category':category,'pagedom':pagedom,'userName':username,'userID':index,'logineduser':logineduser})
            return HttpResponse(t.render(c))
    else:
         c=Context({'posts':post,'category':category,'pagedom':pagedom,'userName':username,'userID':index})
         return HttpResponse(t.render(c))

def createpage(request,index):
    category=BlogCategory.objects.filter(userID=index)
    currentuser=User.objects.get(id=index)
    if category.count()==0:
       cate=BlogCategory(name="未定义",userID=request.session['userID'])
       cate.save()
       category=BlogCategory.objects.filter(userID=index) 
    if currentuser is not None and category is not None:
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
       return HttpResponseRedirect("/blog/"+uid+"/categorymanage")

def articlemanage(request,index):
    if index==str(request.session['userID']):
       loginedname=request.session['userName']
       logineduser=User.objects.get(name=loginedname)
       articles=BlogTable1.objects.filter(userID=request.session['userID'])
       t=loader.get_template("articlemanage.html")
       c=Context({'articles':articles,'userID':request.session['userID'],'logineduser':logineduser})
       return HttpResponse(t.render(c))
    else:
       return HttpResponseRedirect("/blog")

def categorymanage(request,index):
    if index==str(request.session['userID']):
       categorys=BlogCategory.objects.filter(userID=request.session['userID'])
       logineduser=User.objects.get(id=request.session['userID'])
       t=loader.get_template("categorymanage.html")
       c=RequestContext(request,{'categorys':categorys,'userID':index,'logineduser':logineduser})
       return HttpResponse(t.render(c)) 
    else:
       return HttpResponseRedirect("/blog/"+index)

def categoryedit(request,uid):
    if uid==str(request.session['userID']):
       categorys=BlogCategory.objects.filter(userID=uid)
       oldcategory=BlogCategory.objects.get(name=request.POST['oldname'])
       oldarticles=BlogTable1.objects.filter(id=uid,category=oldcategory)
       
       BlogCategory.objects.filter(name=request.POST['oldname']).update(name=request.POST['newname'])
       newcategory=BlogCategory.objects.get(name=request.POST['newname'],userID=uid)
       logineduser=User.objects.get(id=request.session['userID'])
       oldarticles.update(category=newcategory)
       t=loader.get_template("categorymanage.html")
       c=RequestContext(request,{'categorys':categorys,'userID':uid,'logineduser':logineduser})
       return HttpResponse(t.render(c)) 
    else:
       return HttpResponseRedirect("/blog/"+index)


def deletecategory(request,index,string):
    if index==str(request.session['userID']):
       categorys=BlogCategory.objects.get(name=string,userID=index)
       categorys.delete()
       return HttpResponseRedirect("/blog/"+index+"/categorymanage")
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
       return HttpResponseRedirect("/blog/"+uid+"/articlemanage")
    else:
       return HttpResponseRedirect("/blog")

def showeditblogpage(request,uid,index):
    if uid==str(request.session['userID']):
       article=BlogTable1.objects.get(userID=uid,id=index)
       categorys=BlogCategory.objects.filter(userID=uid)
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
          if originarticle.category.name is not None:
          	changeedcag=BlogCategory.objects.get(name=originarticle.category.name)
          	changeedcag.num-=1
         	changeedcag.save()
         	updatecag=BlogCategory.objects.get(name=request.POST['blogcategory'])
         	updatecag.num+=1
         	updatecag.save()
         	time=datetime.datetime.now()
         	BlogTable1.objects.filter(id=index).update(title=request.POST['blogtitle'],body=request.POST['blogcontent'],category=updatecag,timestamp=time)
          else:
                updatecag=BlogCategory.objects.get(name=request.POST['blogcategory'])
         	updatecag.num+=1
         	updatecag.save()
         	time=datetime.datetime.now()
         	BlogTable1.objects.filter(id=index).update(title=request.POST['blogtitle'],body=request.POST['blogcontent'],category=updatecag,timestamp=time)
       return HttpResponseRedirect("/blog/"+uid+"/article/"+index)
    else:
        return HttpResponseRedirect("/blog")
        
class Page():
      startIndex=''
      endIndex=''
      totalRow=''
      onePageRow=''
      pageNum=''
      nowPage=''
      url=''
      def __init__(self,totalRow,onePageRow,pageNum,nowPage,url):
	  onePageRow=int(onePageRow)
	  nowPage=int(nowPage)
          self.startIndex=(nowPage-1)*onePageRow
          if nowPage*onePageRow-1>totalRow:
             self.endIndex=totalRow-1
          else:
	     self.endIndex=nowPage*onePageRow-1
	  self.totalRow=int(totalRow)
      	  self.onePageRow=int(onePageRow)
      	  self.pageNum=int(pageNum)
          self.nowPage=int(nowPage)
          self.url=url
      #参数说明：总记录数，每页的记录数，每次最多现实多少页码，当前页
      def createdom(self):
	  #计算总页数
	  totalPages=int(math.ceil(float(self.totalRow)/float(self.onePageRow)))
	  pageNumArray=[]
	  i=1;
	  pageItem=0;
	  
	  #页面中要显示的页码如1 2 3 4 5 填充到数组中
	  while i<=self.pageNum and pageItem<totalPages:
		pageItem=int((math.ceil(float(self.nowPage)/float(self.pageNum))-1)*self.pageNum+i)
		pageNumArray.append(pageItem)
		i=i+1
	  #根据当前页 计算出其他附属操作如上一页，下一页
	  prePage=''
	  if self.nowPage>1:
	     prePage=self.nowPage-1
	  preGroup=''
	  if pageNumArray[0]>1:
	     preGroup=pageNumArray[0]-self.pageNum

	  nextPage=''
	  if self.nowPage<totalPages:
	     nextPage=self.nowPage+1

	  nextGroup=''
	  pageNum=int(self.pageNum)
	  if pageNumArray[len(pageNumArray)-1]<totalPages:
	     nextGroup=pageNumArray[len(pageNumArray)-1]+1
	    
	  #得到分页栏的DOM并返回
	  pageDOM="<h4>总共有"+str(totalPages)+"页"+str(self.totalRow)+"条记录</h4>"
	  pageDOM+="<div id='pagediv'>"
	  if prePage:
	     pageDOM+="<a href='"+self.url+"/page/"+str(prePage)+"'>上一页</a>"
	  if preGroup:
	     pageDOM+="<a href='"+self.url+"/page/"+str(preGroup)+"'>...</a>"
	  for page in pageNumArray:
	      if self.nowPage==page:
		 pageDOM+="<strong>"+str(page)+"</strong>"
	      else:
		 pageDOM+="<a href='"+self.url+"/page/"+str(page)+"'>"+str(page)+"</a>"
	  if nextGroup:
	     pageDOM+="<a href='"+self.url+"/page/"+str(nextGroup)+"'>...</a>"
          if nextPage:
             pageDOM+="<a href='"+self.url+"/page/"+str(nextPage)+"'>下一页</a>"
	  pageDOM+="</div>"

	  return pageDOM
    
       
       





    
    

