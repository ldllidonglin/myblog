from django.db import models
from django.contrib import admin
class BlogCategory(models.Model):
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
      title=models.CharField(max_length=150)
      body=models.TextField()
      category=models.ForeignKey(BlogCategory)
      tag=models.CharField(max_length=100)
      timestamp=models.DateTimeField()
      def __unicode__(self):
          return self.title


admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(BlogTable1)
# Create your models here.
