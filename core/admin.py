from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils import timezone
from django import forms

# Register your models here.

from core.models import  SiteSetting, Attachment,  CustomField


 

class CustomFieldInlineAdmin( GenericTabularInline):
    model = CustomField
    fields = ('meta_key', 'meta_value' )
    extra = 1

class AttachmentInlineAdmin( GenericTabularInline):
    model = Attachment
    fields = ('guid', 'title' )
    extra = 1


class AttachmentAdmin(admin.ModelAdmin):
    model = Attachment
    inlines = []
    list_display = ['title', 'type']

class AbstractNodeModelAdmin(admin.ModelAdmin):
    # model = StaticPage
    view_on_site = True
    list_display = ['title', 'created_at', 'status',  "view_on_site_link"]
    readonly_fields = ['updated_at']
    inlines = [AttachmentInlineAdmin, CustomFieldInlineAdmin]

    def view_on_site(self,obj):
        return  obj.get_absolute_url()

    def view_on_site_link(self, obj):
        return mark_safe('<a href="{}" target="_blank">View</a>'.format( self.view_on_site(obj)))
    
    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.updated_by = request.user
            obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)
    
    class Meta:
        abstract = True

admin.site.register(SiteSetting)
admin.site.register(Attachment, AttachmentAdmin)