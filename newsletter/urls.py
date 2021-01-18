from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from .views import SubscriberFormView, UnSubscriberFormView


app_name='newsletter'

urlpatterns = [
    path('subscribe/', SubscriberFormView.as_view(), name='subscribe_view'),
    path('unsubscribe/', UnSubscriberFormView.as_view(), name='unsubscribe_view'),
]

