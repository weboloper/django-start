from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.http import Http404
from blog.models import StaticPage, Post, Category, Comment
from blog.forms import CommentForm
from django.views.generic.edit import FormMixin, FormView

# Create your views here.
class StaticPageView(DetailView):
    template_name = 'blog/static_page.html'
    model = StaticPage

    def get_object(self):

        if 'full_slug' in self.kwargs:
            full_slug = self.kwargs['full_slug']
            slugs = full_slug.split('/')
            page_slug = slugs[-1]
    
            obj =  get_object_or_404(self.model, slug=page_slug)
    
            if obj.is_viewable(self.request.user):
                if obj.is_published() == False:
                    messages.add_message(self.request, messages.INFO, _('Page is not viewable : '+ obj.get_status_display()))
                return obj
        
        raise  Http404()


class PostListView(ListView):
    template_name = 'blog/post/post_list.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 4 

    def get_queryset(self):
        return self.model.objects.published()

class PostDetailView(FormMixin, DetailView):
    template_name = 'blog/post/post_detail.html'
    model = Post
    context_object_name = 'post'
    form_class = CommentForm
    success_url= '/'

    def get_object(self):
    
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')
        pk = self.kwargs.get('pk')

        if pk:
            obj =  get_object_or_404(Post, pk=self.kwargs.get('pk'))
        else:
            obj = get_object_or_404(
                Post,
                published_at__year=year,
                published_at__month=month,
                published_at__day=day,
                slug=slug
            )
            
        if obj.is_viewable(self.request.user):
            if obj.is_published()== False:
                messages.add_message(self.request, messages.INFO, _('Post is not viewable'))
            return obj
        else:
            raise  Http404()
        
    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(entry=self.object, is_public=True)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = self.get_object()
            comment.save()
            return self.form_valid(form)
        else:
            print("Invalid form")
            return self.form_invalid(form)
    
class PostByCategoryListView(ListView):
    template_name = 'blog/post/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False
    model = Post
    allow_empty=True

    def get_queryset(self):
        return self.model.objects.list_by_category_slug(self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['category'] = category
        return context
 

# class CategoryDetailView(DetailView):
#     # https://github.com/hishamad/Blog/blob/4e5a410053f7767d4ffd61ba6120e6c0b79bc2d1/blog_project/blog/views.py
#     model = Category
#     template_name = 'blog/post_list.html'
#     context_object_name = 'category'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         page = self.request.GET.get('page')
#         # posts = paginator = Paginator(Post.objects.filter(category_id=self.kwargs.get('pk')).order_by('-date_posted'), 2)
#         posts = Post.objects.list_by_category( self.object )
#         context['posts'] = posts
#         return context