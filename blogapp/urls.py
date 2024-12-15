from django.urls import path
from . import views

urlpatterns = [
    path("blog/",views.blog,name='blog'),
    path('blog/<slug:url>/',views.blog_details,name='blog_details'),
    path('category/<slug:category_url>/',views.post_list_by_category,name="post_list_by_category"),
    path('tag/<slug:tag_url>/',views.post_list_by_tags,name="post_list_by_tags"),
    path('search/',views.blog_search,name="blog_search"),
    path('postcomment',views.postcomment,name="postcomment")
]
