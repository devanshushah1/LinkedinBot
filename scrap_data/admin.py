from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display = ['id', 'name', 'heading', 'link', 'company', 'position', 'message']

admin.site.register(Profile, ProfileAdmin)

class LinkedInPostsAdmin(admin.ModelAdmin):
    model = LinkedInPosts
    list_display = ['post_link','text', 'posted_at']

admin.site.register(LinkedInPosts, LinkedInPostsAdmin)

class MessageAdmin(admin.ModelAdmin):
    model=Message
    list_display = ['id','bookmark', 'text']

admin.site.register(Message, MessageAdmin)

class YelpAdmin(admin.ModelAdmin):
    model = Business
    list_display = ['name', 'number', 'address', 'date', 'visit_site', 'city', 'state', 'zip', 'country',
                    'search_term', 'email' ,'source' , 'source_url']


admin.site.register(Business, YelpAdmin)

class FaceBookAdmin(admin.ModelAdmin):
    model = Facebook
    list_display = ['post_link', 'photo_link', 'date_time', 'header']

admin.site.register(Facebook, FaceBookAdmin)

class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ['url', 'post']

admin.site.register(Image, ImageAdmin)

class GIFAdmin(admin.ModelAdmin):
    model = GIF
    list_display = ['url', 'post']

admin.site.register(GIF, GIFAdmin)
