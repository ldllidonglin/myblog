from django.db import models
from django.contrib import admin
from DjangoUeditor.models import UEditorField

class User(models.Model):
      name=models.CharField(max_length=30)
      password=models.CharField(max_length=30)
      def __unicode__(self):
          return self.name

class BlogCategory(models.Model):
      userID=models.CharField(max_length=30)
      name=models.CharField(max_length=30,primary_key=True)
      num=models.IntegerField(max_length=10,default="0")
      def __unicode__(self):
        return self.name

class BlogPost(models.Model):
      title=models.CharField(max_length=150)
      body=models.TextField()
      tag=models.CharField(max_length=100)
      timestamp=models.DateTimeField()
      def __unicode__(self):
          return self.title
class BlogTable1(models.Model):
      userID=models.CharField(max_length=10)
      userName=models.CharField(max_length=30)
      title=models.CharField(max_length=150)
      body=UEditorField(width=600, height=300, toolbars="full")
      category=models.ForeignKey(BlogCategory,default="0")
      tag=models.CharField(max_length=100)
      timestamp=models.DateTimeField()
      def __unicode__(self):
          return self.title


admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(BlogTable1)
admin.site.register(User)
# Create your models here.
