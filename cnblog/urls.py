"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^up_down/$',views.Up_down.as_view()),
    url(r'^comment/$',views.Sub_comment.as_view()),
    url(r'^backend/$',views.Backend.as_view()),
    url(r'^addarticle/$',views.Addarticle.as_view()),
    url(r'^cnblog.com/', include('blog.urls')),
    url(r'^article/', include('blog.urls')),
    url(r'^validcode/',views.get_valid_img),
]
