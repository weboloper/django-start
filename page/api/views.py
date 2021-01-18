from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, GenericAPIView
from page.models import Page
from page.api.serializers import *
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response


class PageDetailView(RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = 'slug'
    model = Page

