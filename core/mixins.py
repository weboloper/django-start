from django.db import models

# from core.managers import CurrentSiteManager
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.utils.translation import gettext_lazy as _
from core.utils import   unique_slug , upload_location
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
import json
from tinymce.models import HTMLField
from django.urls import reverse

class SiteRelated(models.Model):
    class Meta:
        abstract = True
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='aaa')
    # objects = models.Manager()
    # on_site = CurrentSiteManager()
    
    # def save(self, update_site=False, *args, **kwargs):
    #     if update_site or not self.id:
    #         self.site_id = current_site_id()
    #     super(SiteRelated, self).save(*args, **kwargs)

    

class GenericMixin(models.Model):
    class Meta:
        abstract = True

    content_type = models.ForeignKey(ContentType, blank=True,null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True,null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

class SlugMixin(models.Model):

    class Meta:
        abstract = True

    slugify_field = 'title'
    title = models.CharField(_("Title"), max_length=256)
    slug = models.SlugField(_("URL"),
        max_length=256,
        blank=True,
        help_text=_("Leave blank to have the URL auto-generated from " "the title."),)
    def get_slug(self):
        try:
            slugify_field_value = getattr(self, self.slugify_field)
        except AttributeError:
            raise AttributeError("Field '%s' was marked as field to be used as slug, but does not exist in '%s'" %
                                 (self.slugify_field, self.__class__.__name__))
        return slugify(slugify_field_value)
 
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(SlugMixin, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        Klass = self.__class__
        slug_qs = Klass.objects.exclude(id=self.id)
        return unique_slug(slug_qs, "slug", self.get_slug())



    
class AuditMixin(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Created by"),
                                   related_name="%(app_label)s_%(class)s_created_related", default=1, on_delete=models.SET_DEFAULT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Updated by"),
                                    related_name="%(app_label)s_%(class)s_updated_related",
                                    null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated on"), null=True, blank=True, auto_now=True)
    class Meta:
        abstract = True

    def is_editable(self, request):
        """
        Restrict in-line editing to the objects's owner and superusers.
        """
        return request.user.is_superuser or request.user.id == self.created_by_id
    

class PublishMixin(models.Model):
    class Meta:
        abstract = True

    CONTENT_STATUS_TRASH = 'trash'
    CONTENT_STATUS_DRAFT = 'draft'
    CONTENT_STATUS_PUBLISHED = 'publish'
    CONTENT_STATUS_CHOICES = (
        (CONTENT_STATUS_DRAFT, _("Draft")),
        (CONTENT_STATUS_PUBLISHED, _("Published")),
        (CONTENT_STATUS_TRASH, _("Trash")),
    )

    status = models.CharField(
        _("Status"),
        choices=CONTENT_STATUS_CHOICES,
        default=CONTENT_STATUS_PUBLISHED,
        help_text=_(
            "With Draft chosen, will only be shown for admin users " "on the site."
        ),
        max_length=20
    )

    published_at = models.DateTimeField(
        _("Published from"),
        help_text=_("With Published chosen, won't be shown until this time"),
        blank=True,
        null=True,
        db_index=True,
    )

    expired_at = models.DateTimeField(
        _("Expires At"),
        help_text=_("With Expired chosen, won't be shown after this time"),
        blank=True,
        null=True,
        db_index=True,
    )
    
    featured_at = models.DateTimeField(
        _("Featured at"),
        help_text=_("With Featured chosen, will set featured from this time"),
        blank=True,
        null=True,
        db_index=True,
    )

    def is_featured(self):
        if featured_at:
            return True
        return False

    def is_published(self):
        """
        Checks if an entry is within his publication period.
        """
        if  self.status != PublishMixin.CONTENT_STATUS_PUBLISHED:
            return False
        now = timezone.now()
        if self.published_at and now < self.published_at  :
            return False
        if self.expired_at and now > self.expired_at :
            return False
        return True
    
    def is_viewable(self, user):
        if self.is_published():
            return True
        
        return (self.created_by == user or
                user.is_staff 
                )

    def save(self, *args, **kwargs):
        if self.status == self.CONTENT_STATUS_PUBLISHED  and not self.published_at:
            self.published_at = timezone.now()
        return super(PublishMixin, self).save(*args, **kwargs)

class FeaturedImageMixin(models.Model):
    class Meta:
        abstract = True

    featured_image = models.ForeignKey( 'core.Attachment' ,  db_column='object_id' , null=True, blank=True, verbose_name=_("featured_image"), on_delete=models.SET_NULL)

class ContentMixin(models.Model):
    class Meta:
        abstract = True

    content = HTMLField(_("Content body"),  blank=True,null=True)
    excerpt = models.TextField(_("Excerpt"), max_length=1500,blank=True,null=True)


class CustomFieldMixin( models.Model ):
    class Meta:
        abstract = True

    custom_fields = GenericRelation( "core.CustomField" )
    
    def get_meta_data(self, meta_key, unique=True ):
        if unique == True:
            return self.custom_fields.filter(meta_key=meta_key).first()
        else:
            return self.custom_fields.filter(meta_key=meta_key).only('meta_value').all()

    @staticmethod
    def validateJSON (jsonData):
        try:
            json.loads (jsonData)
        except ValueError as err:
            return False
        return True


    def get_meta(self, meta_key, unique=True ):
        meta = self.get_meta_data(meta_key, unique )
        if meta:
            if unique:
                if self.validateJSON( meta.meta_value):
                    return json.loads(meta.meta_value) 
                else:
                    return meta.meta_value
            else:
                meta_list = []
                for meta in meta.all():
                    meta_list.append(meta.meta_value)
                return meta_list
 
        return ''


class NodeTypeMixin(models.Model):
    class Meta:
        abstract = True
    
    NODE_TYPE_POST = 'post'
    NODE_TYPE_NEWS = 'news'
    NODE_TYPE_CHOICES = (
        (NODE_TYPE_POST, _("Blog Post")),
        (NODE_TYPE_NEWS, _("News Post")),
    )

    node_type = models.CharField(
        _("Node Type"),
        max_length=20,
        choices=NODE_TYPE_CHOICES,
        default=NODE_TYPE_POST,
        help_text=_(
            "Node type that will be used."
        ),
        db_index=True
    )


class AbstractNodeModel(SlugMixin, ContentMixin, AuditMixin, PublishMixin, FeaturedImageMixin, CustomFieldMixin ):
    
    def url_to_edit_object(self):
        return  reverse('admin:%s_%s_change' % (self._meta.app_label,  self._meta.model_name),  args=[self.id] )

    class Meta:
        abstract = True