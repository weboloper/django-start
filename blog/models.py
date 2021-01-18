from django.db import models
from django.forms import ValidationError
from blog.managers import BaseEntryManager ,PostManager,  NewsEntryManager 
from core.mixins import GenericMixin, SlugMixin, SiteRelated , AbstractNodeModel, NodeTypeMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.timezone import localtime
from taggit.managers import TaggableManager
from django.conf import settings
from django.contrib.sites.models import Site


class Category(SlugMixin):

    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children', on_delete=models.CASCADE
    )
    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])

    def get_children(self):
        return Category.objects.filter(parent=self)
    
    @classmethod
    def get_root(cls):
        return cls.objects.get(parent=None)
    
    def get_absolute_url(self):
        full_path = [self.slug]
        k = self.parent
        while k is not None:
            full_path.append(k.slug)
            k = k.parent
        return '/category/' + '/'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        # prevent a category to be itself parent
        if self.id and self.parent and self.id == self.parent.id:
            # raise ValidationError('You can\'t have yourself as a parent!')
            self.parent = None
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class BaseEntry(AbstractNodeModel, NodeTypeMixin):
    categories = models.ManyToManyField(
        Category, related_name='%(app_label)s_%(class)s_entries', blank=True
    )
    tags = TaggableManager(related_name='posts', blank=True)

    def get_absolute_url(self):
        return None
 

class Post(BaseEntry):
    limit_to_post_type = BaseEntry.NODE_TYPE_POST
    
    objects = PostManager()

    class Meta:
        proxy = True
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")

    def save(self, *args, **kwargs):
        self.node_type = self.limit_to_post_type
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
     
        # if self.published_at:
        local_publish = localtime(self.published_at)
        return reverse('blog:posts_detail',  kwargs={
                    'year': local_publish.year, 
                    'month': local_publish.month, 
                    'day': local_publish.day, 
                    'slug' :self.slug 
                    }
                )
        # return reverse('blog:posts_detail_by_id',  kwargs={'pk': self.pk })

class NewsEntry(BaseEntry):
    limit_to_post_type = BaseEntry.NODE_TYPE_NEWS
    objects = NewsEntryManager()

    class Meta:
        proxy = True
        verbose_name = _("News")
        verbose_name_plural = _("News")

    def save(self, *args, **kwargs):
        self.node_type = self.limit_to_post_type
        super(NewsEntry, self).save(*args, **kwargs)


class Comment(models.Model):
    user_name   = models.CharField(_("name"), max_length=50)
    user_email  = models.EmailField(_("email address"))
    user_url    = models.URLField(_("homepage"), blank=True)
    
    comment = models.TextField(_('comment'), max_length=500)
    
    ip_address  = models.GenericIPAddressField(_('ip address'), blank=True, null=True)
    useragent  = models.CharField(_("user agent string"), max_length=100, blank=True, null=True)
    
    entry = models.ForeignKey(BaseEntry, related_name='parent', on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name='children',default=None,null=True,blank=True, on_delete=models.CASCADE)
    
    is_public = models.BooleanField(_('is public'), default = True)
    is_notice = models.BooleanField(_('receive email notify'), default = True)
    
    created_at = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated on"), null=True, blank=True, auto_now=True)
    
    #Inspired by http://www.djangosnippets.org/snippets/112/
    # &http://www.voidspace.org.uk/python/modules.shtml#akismet
    def comment_check(self):
        '''
        Check a comment.
        Return True for ham, False for spam.
        Use this function before save a comment.
        '''
        try:
            if hasattr(settings, 'BAN_NON_CJK') and settings.BAN_NON_CJK:
                import re
                if not re.search("[\u4E00-\u9FC3\u3041-\u30FF]",self.comment):
                    raise Exception()
                
            if hasattr(settings, 'AKISMET_API_KEY') and settings.AKISMET_API_KEY:
                from akismet import Akismet
                akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url='http://%s/' % Site.objects.get_current().domain)
                if akismet_api.verify_key():
                    akismet_data = { 'comment_type': 'comment',
                                    'user_ip':self.ip_address,
                                    'user_agent':self.user_agent,
                                    'referrer':'',
                                    }
                    return not akismet_api.comment_check(self.comment.encode("utf8"), data=akismet_data, build_data=True)
            else:
                return True
        except:
            return False

    class Meta:
        ordering = ['-updated_at']
        
    def __unicode__(self):
        return self.comment