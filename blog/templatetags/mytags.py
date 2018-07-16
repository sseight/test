from django import template
from django.db.models import Count
from blog.models import *
register=template.Library()


@register.inclusion_tag("left.html")
def left(user):
    category_list = Category.objects.filter(blog=user.blog).annotate(c=Count("article")).values("title", "c")
    tag_list = Tag.objects.filter(blog=user.blog).annotate(c=Count("article")).values("title", "c")
    date_list = Article.objects.extra(select={"date": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("date").annotate(c=Count("title")).values_list("date", "c")
    return {"category_list":category_list,"tag_list":tag_list,"date_list":date_list,"username":user.username}