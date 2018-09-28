#coding:utf-8
from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class AuthorDetails(models.Model):
    age = models.IntegerField()
    email = models.CharField(max_length=50)
    sex = models.IntegerField(choices=((0, '男'), (1, '女')))
    phone = models.CharField(max_length=15)
    author = models.OneToOneField(Author)

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    website = models.URLField()
    def __unicode__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    #DateField是年月日（DateTimeField是年月日时分秒）
    publication_date = models.DateField()
    #价格是float类型
    price = models.FloatField(max_length=20)
    #书和出版社的关系：多对一，也就是外键关系
    publisher = models.ForeignKey(Publisher)
    #书和作者的关系：多对多
    author = models.ManyToManyField(Author)


