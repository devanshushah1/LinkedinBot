from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Message(models.Model):
    text=models.TextField(max_length=500 , blank=True , null=True)
    bookmark=models.BooleanField(max_length=2, blank=True, null=True)

    def __str__(self):
        return str(self.text)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    link=models.URLField(max_length=100,blank=True,null=True)
    name=models.CharField(max_length=100, default="",null=True,blank=True)
    heading=models.TextField(max_length=200,default="",null=True,blank=True)
    position=models.CharField(max_length=50,blank=True,null=True,default="")
    company=models.CharField(max_length=50,null=True,blank=True,default="")
    message=models.ForeignKey(Message, on_delete=models.CASCADE , null=True , blank=True)
    is_friend=models.BooleanField(max_length=2, null=True , blank=True)
    mutual=models.ManyToManyField("self",symmetrical=False)
    extracted_datetime = models.DateTimeField(default=datetime.datetime.now(), null=True, blank=True)

    def __str__(self):
        return str(self.name)

class LinkedInPosts(models.Model):
    post_link = models.URLField(max_length=500, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    posted_at = models.CharField(max_length=20, null=True, blank=True)
    date_added_to_database = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Business(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.datetime.now())
    visit_site = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    search_term = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    source_url = models.URLField(max_length=500,null=True,blank=True)
    sources=[('Yelp','Yelp'),('Yellow','Yellow')]
    source = models.CharField(max_length=6,choices=sources,null=True,blank=True)

class Facebook(models.Model):
    post_link = models.URLField(max_length=500, blank=True, null=True)
    date_time = models.CharField(max_length=20, blank=True, null=True)
    header = models.CharField(max_length=50, blank=True, null=True)
    photo_link = models.URLField(max_length=500, blank=True, null=True)

class Image(models.Model):
    url = models.URLField(max_length=500, blank=True, null=True)
    post = models.ForeignKey(Facebook, null=True, blank=True, on_delete=models.CASCADE)

class GIF(models.Model):
    url = models.URLField(max_length=500, blank=True, null=True)
    post = models.ForeignKey(Facebook, null=True, blank=True, on_delete=models.CASCADE)