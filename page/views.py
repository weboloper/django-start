from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.http import Http404
from page.models import Page

# Create your views here.
class PageDetailView(DetailView):
    template_name = 'blog/static_page.html'
    model = Page

    def get_object(self):

        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            slugs = slug.split('/')
            page_slug = slugs[-1]
    
            obj =  get_object_or_404(self.model, slug=page_slug)

            if obj.get_absolute_url()[1:] != slug:
                raise  Http404()
    
            if obj.is_viewable(self.request.user):
                if obj.is_published() == False:
                    messages.add_message(self.request, messages.INFO, _('Page is not viewable : '+ obj.get_status_display()))
                return obj
        
        raise  Http404()


# Create your views here.
# https://github.com/jamiecurle/designcc-core/blob/d5d10f762fd766b90900aa9a83ad854dcc835435/cc/pages/views.py
# if slug is None:
#         try:
#             page = Page.objects.visible()[:1][0]
#         except (Page.DoesNotExist, IndexError):
#             raise Http404("No pages to display")
#     else:
#         page = get_object_or_404(Page, slug=slug, visible=True)


# https://github.com/CivilHub/CivilHub/blob/97c3ebe6031e6a3600c09d0fd99b764448ca592d/staticpages/views.py
# if self.page: page = self.page
#         if page == None:
#             return render(request, 'staticpages/pages/home.html')
#         else:
#             try:
#                 template_name = 'staticpages/pages/' + page + '.html'
#                 return render(request, template_name)


# https://github.com/Filon/drobservis/blob/c9c28434561cc04ac9f1f137dc37fbea9430d7c8/pages/views.py
# check url is same

# https://github.com/waustin/django_2_starter_template/blob/e611c0359ac294be16e9a34b1a799ac90a01e994/apps/pages/models.py
# template mantığı,


# https://github.com/mac2394q/gecolsa-source-website/blob/fd2d7e48a4df16ba328dd7a39b85fce3595c2476/cms/models.py

# https://github.com/Rockstreet/newsusman/blob/923a00beafb8a9f82a3acc0f3b2b183bf5bb3d52/page/models.py
# desc from excerpt

# https://www.djangosnippets.org/snippets/362/