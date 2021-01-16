from django.urls import path, include, re_path
from blog.api.views import PostListAPIView, PostDetailView, FeaturedPostListAPIView,  CategoryDetailView

urlpatterns = [
    path('featured/', FeaturedPostListAPIView.as_view(), name='featured_list_api'),
    path('posts/', PostListAPIView.as_view(), name='post_list_api'),
    path('posts/<slug>', PostDetailView.as_view(), name='post_detail_api'),
    path('category/<slug>/posts/', CategoryDetailView.as_view(), name='category_detail_api'),
]
