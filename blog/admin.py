from django.contrib import admin
from blog.models import   Post, NewsEntry, Category, Comment
from core.admin import AbstractNodeModelAdmin
from django.utils.html import mark_safe
# Register your models here.

 
class PostAdmin(AbstractNodeModelAdmin):
    model = Post
    pass

class NewsAdmin(AbstractNodeModelAdmin):
    model = NewsEntry
    pass

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    view_on_site = True
    list_display = ['__str__' , 'view_on_site_link']

    def view_on_site(self,obj):
        return  obj.get_absolute_url()

    def view_on_site_link(self, obj):
        return mark_safe('<a href="{}" target="_blank">View</a>'.format( self.view_on_site(obj)))
    


admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(NewsEntry, NewsAdmin)
