from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, GenericAPIView
from blog.models import Post, Category
from blog.api.serializers import *
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

class PostListAPIView(ListAPIView):
    model = Post
    serializer_class = PostSerializer
    lookup_field = 'slug'
    paginate_by = 4 
    
    
    def get_queryset(self):
        return self.model.objects.published()

    # def get_serializer_context(self):
    #     return {
    #         'request' : self.request,
    #         'posts': self.get_queryset()
    #     } 

class FeaturedPostListAPIView(ListAPIView):
    model = Post
    serializer_class = PostSerializer
    lookup_field = 'slug'
    paginate_by = 4 
    
    
    def get_queryset(self):
        return self.model.objects.featured()

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    model = Post

class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'slug'
    model = Category
    
