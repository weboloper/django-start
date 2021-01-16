from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static

from main.views import IndexPageView, ChangeLanguageView
from blog.views import StaticPageView
from core.api.views import upload_attachment_url

from blog.sitemaps import StaticPageSitemap, PostSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {'pages': StaticPageSitemap, 'posts' : PostSitemap }

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexPageView.as_view(), name='index'),

    path('upload_attachment_url/', upload_attachment_url),

    

    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),

    path('tinymce/', include('tinymce.urls')),

    path('blog/', include('blog.urls')),
    
    
    re_path(r'^(?P<full_slug>(.*))/$', StaticPageView.as_view(), name='static_page' ),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
