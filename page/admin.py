from django.contrib import admin
from page.models import  Page
from core.admin import AbstractNodeModelAdmin
# Register your models here.

class PageAdmin(AbstractNodeModelAdmin):
    model = Page
    pass

admin.site.register(Page, PageAdmin)