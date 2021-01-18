from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from page.models import Page

class PageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    def items(self):
        return Page.objects.published()
    
