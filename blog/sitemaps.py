from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.objects.published()