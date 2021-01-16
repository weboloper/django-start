from django.views.generic import TemplateView, DetailView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import render, get_object_or_404


class IndexPageView(TemplateView):
    template_name = 'main/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


