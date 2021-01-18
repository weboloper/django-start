from django.urls import path, include, re_path
from page.views import PageDetailView

urlpatterns = [
    re_path(r'^(?P<slug>(.*))/$', PageDetailView.as_view(), name='page-detail' ),
]