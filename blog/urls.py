from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from blog.views import PostListView, PostByCategoryListView,  PostDetailView
# from blog.models import StaticPage

app_name='blog'

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    # path('category/<slug>', PostByCategoryListView.as_view(), name='posts_by_category_list'),
    re_path(r'^category/(?P<slug>(.*))/$', PostByCategoryListView.as_view(), name='posts_by_category_list'),
    
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',  PostDetailView.as_view(), name='posts_detail'),
    path('posts/<pk>',  PostDetailView.as_view(), name='posts_detail_by_id'),

    # path('api/', include('blog.api.urls')),
]

