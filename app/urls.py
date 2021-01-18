from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static

from main.views import IndexPageView, ChangeLanguageView
from core.api.views import upload_attachment_url

#sitemaps
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from page.sitemaps import PageSitemap
sitemaps = {'pages': PageSitemap, 'posts' : PostSitemap }

# from django.conf.urls import include, url, handler404, handler500, handler403, handler400, re_path
# handler404 
urlpatterns = [
    #default
    path('', IndexPageView.as_view(), name='index'),
    path('upload_attachment_url/', upload_attachment_url),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),
    path('admin/', admin.site.urls),
    
    #vendors
    path('tinymce/', include('tinymce.urls')),

    #apps
    
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('newsletter/', include('newsletter.urls')),
    
    #apis
    path('api/blog/', include('blog.api.urls')),
    path('api/', include('page.api.urls')),

    #page module 
    path('',  include('page.urls') ),

    #sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
