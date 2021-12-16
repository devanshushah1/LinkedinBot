"""linkedin_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scrap_data.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('linkedin/',linkedin.as_view(), name='linkedin'),
    path('linkedin_posts/', linked_in_posts, name='linkedin_posts'),
    path('linkedin_posts_delete/', linkedin_posts_delete, name='linkedin_posts_delete'),
    path('connectbutton/',connectbutton.as_view(), name='connect'),
    path('userconnection/',userconnection.as_view(), name='userconnection'),
    path('yellow/', yellow.as_view(), name='yellow'),
    path('facebook/', facebook, name='facebook'),
    path('delete-facebook/', delete_facebook, name='delete_facebook'),
]
