from django.urls import path, include, re_path
from page.api.views import PageDetailView

urlpatterns = [
    path('pages/<slug>', PageDetailView.as_view(), name='page_detail_api'),
]
