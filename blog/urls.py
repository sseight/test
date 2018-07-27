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
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.Index.as_view()),
    url(r'^login/$',views.Login.as_view()),
    url(r'^logout/$',views.Logout.as_view()),
    url(r'^register/$',views.Register.as_view()),

    url(r'^site/(?P<username>\w+)/(?P<condition>category|tag|date)/(?P<param>.*)/$',views.Homesite.as_view()),
    url(r'^site/(?P<username>\w+)/$',views.Homesite.as_view()),
    url(r'^site/(?P<username>\w+)/article/(?P<article_id>\d+)/$',views.Article_detail.as_view()),
    url(r'^edit/(?P<article_id>\d+)/$',views.Editor.as_view()),
]
