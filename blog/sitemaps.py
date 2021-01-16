from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import StaticPage, Post

class StaticPageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    def items(self):
        return StaticPage.objects.published()
    

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.objects.published()