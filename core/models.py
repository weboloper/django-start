from django.db import models
from core.mixins import GenericMixin, SlugMixin, SiteRelated , AbstractNodeModel, NodeTypeMixin
from django.utils.translation import gettext_lazy as _
from core.utils import   unique_slug , upload_location
import os 
from django.contrib.sites.models import Site
from django.conf import settings
from PIL import Image
import os, random, hashlib
from django.core.files.base import ContentFile
from io import BytesIO
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
import json 
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sites.managers import CurrentSiteManager
from django.forms import ValidationError
from sorl.thumbnail import get_thumbnail
from core.managers import BlogEntryManager,  NewsEntryManager

class SiteSettingManager(models.Manager):
    def get_current(self):
        if SiteSetting.objects.filter(site = Site.objects.get_current()):
            return SiteSetting.objects.filter(site = Site.objects.get_current())[0]
        return None

class SiteSetting(models.Model):
    title = models.CharField(_('Title'),max_length=100)
    slogan = models.CharField(_('Slogan'),max_length=255)
    description = models.TextField(_('description'))
    keywords = models.CharField(_('Keyword'),max_length=100)
    site = models.OneToOneField(Site,default=settings.SITE_ID, on_delete=models.CASCADE)
    feed = models.URLField(_('Custom Feed URL'), blank=True)
    
    facebook = models.URLField(_("Facebook"), max_length=200, blank=True)
    twitter = models.URLField(_("Twitter"), max_length=200, blank=True)
    instagram = models.URLField(_("Instagram"), max_length=200, blank=True)
    youtube = models.URLField(_("Youtube"), max_length=200, blank=True)
    linkedin = models.URLField(_("LinkedIn"), max_length=200, blank=True)
    
    objects = SiteSettingManager()
    # on_site = CurrentSiteManager()
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title
    


AUDIO_TYPE = 'a'
DOCUMENT_TYPE = 'd'
IMAGE_TYPE = 'i'
VIDEO_TYPE = 'v'
OTHER_TYPE = 'x'
TYPE_CHOICES = (
    (AUDIO_TYPE, 'audio'),
    (DOCUMENT_TYPE, 'document'),
    (IMAGE_TYPE, 'image'),
    (VIDEO_TYPE, 'video'),
    (OTHER_TYPE, 'other'),
)


AUDIO_MIME_TYPES = [
    'audio/aiff',
    'audio/aac',
    'audio/midi',
    'audio/mpeg',
    'audio/mp4',
    'audio/ogg',
    'audio/wav',
    'audio/x-wav',
    'audio/x-ms-wma',
    'audio/flac',
    'audio/x-matroska',
    'audio/basic',
]
DOCUMENT_MIME_TYPES = [
    'application/pdf',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.ms-excel',
    'application/vnd.ms-powerpoint',
    'application/vnd.ms-word',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/rtf',
]
IMAGE_MIME_TYPES = [
    'image/bmp',
    'image/gif',
    'image/jpeg',
    'image/jp2',
    'image/png',
    'image/webp',
    'image/x-icon',
    'image/vnd.adobe.photoshop',
    'image/tiff',
]
VIDEO_MIME_TYPES = [
    'video/3gpp2',
    'video/3gpp',
    'video/avi',
    'video/x-flv',
    'video/mp4',
    'video/x-matroska',
    'video/quicktime',
    'video/mpeg',
    'video/dvd',
    'video/x-ms-wmv',
    'video/x-ms-asf',
    'video/ogg',
    'video/webm',
]


MIME_TYPE_TO_TYPE = {
    **{k: AUDIO_TYPE for k in AUDIO_MIME_TYPES},
    **{k: DOCUMENT_TYPE for k in DOCUMENT_MIME_TYPES},
    **{k: IMAGE_TYPE for k in IMAGE_MIME_TYPES},
    **{k: VIDEO_TYPE for k in VIDEO_MIME_TYPES},
}

class AbstractFileModel( GenericMixin ):
    class Meta:
        abstract = True
    
    title = models.CharField(_("Title"), max_length=256,  blank=True, null=True)
    slug = models.SlugField(_("URL"),
        max_length=256,
        blank=True,
        help_text=_("Leave blank to have the URL auto-generated from " "the title."),)

    guid = models.FileField(_("File"), upload_to=upload_location )
    created_at = models.DateTimeField(auto_now_add=True)
    mime_type = models.CharField(max_length=100, blank=True )
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, default=OTHER_TYPE)
    data = models.TextField(_("Data"), blank=True, null=True )

    __original_guid = None
    def __init__(self, *args, **kwargs):
        super(AbstractFileModel, self).__init__(*args, **kwargs)
        self.__original_guid = self.guid
        
    def save(self, *args, **kwargs):
        if not self.pk or  (self.guid and self.guid != self.__original_guid):
            self.check_mime_type()
        
        if self.title is None :
            filename = os.path.basename(self.guid.path)

            self.title = filename
        super().save(*args, **kwargs)

    def check_mime_type(self):
        if self.guid:
            self.mime_type = self.guid.file.content_type
            self.type = self.get_type_for_mime_type(self.mime_type)

    def get_type_for_mime_type(self, mime_type):
        try:
            return MIME_TYPE_TO_TYPE[mime_type]
        except KeyError:
            return OTHER_TYPE

    def get_image(self, geometry, crop='center'):
        if crop:
            thumbnail = get_thumbnail(self.guid, geometry, crop=crop)
        else:
            thumbnail = get_thumbnail(self.guid, geometry)
        return thumbnail

    def get_image_url(self, geometry, crop='center'):
        image = self.get_image(geometry, crop)
        return image.url

    def get_image_size(self, geometry, crop='no_crop'):
        if 'x' in geometry:
            components = geometry.split('x')
            width = int(components[0])
            height = int(components[1])
            if self.width <= width and self.height <= height:
                return (self.width, self.height)

            if crop == 'no_crop':
                ratio = float(height) / float(width)
                image_ratio = float(self.height) / float(self.width)
                if image_ratio <= ratio:
                    return (width, int(width*image_ratio))
                else:
                    return (int(height/image_ratio), height)
        else:
            width = int(geometry)
            if self.width <= width:
                return (self.width, self.height)
            else:
                image_ratio = float(self.height) / float(self.width)
                return (width, int(width*image_ratio))

        return (width, height)

    def __str__(self):
        return self.title




class Attachment(AbstractFileModel):
    pass



class CustomField(GenericMixin):
    meta_key = models.CharField(_("Meta Key"), max_length=50)
    meta_value = models.TextField(_("Meta Value"))

