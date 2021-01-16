from django.contrib import admin
from blog.models import  StaticPage, Post, NewsEntry, Category, Comment
from core.admin import AbstractNodeModelAdmin
# Register your models here.

class StaticPageAdmin(AbstractNodeModelAdmin):
    model = StaticPage
    pass

class PostAdmin(AbstractNodeModelAdmin):
    model = Post
    pass

class NewsAdmin(AbstractNodeModelAdmin):
    model = NewsEntry
    pass
 


admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(NewsEntry, NewsAdmin)
admin.site.register(StaticPage, StaticPageAdmin)