from django.db import models
from django.forms import ValidationError
from blog.managers import BaseEntryManager ,PostManager,  NewsEntryManager
from core.mixins import GenericMixin, SlugMixin, SiteRelated , AbstractNodeModel, NodeTypeMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.timezone import localtime
from taggit.managers import TaggableManager

class StaticPage(AbstractNodeModel):

    parent = models.ForeignKey( "StaticPage" , verbose_name=_("Parent"),  on_delete=models.CASCADE, null=True, blank=True)

    def parental_path(self):
        url = "/%s/" % self.slug
        page = self
        while page.parent:
            url = "/%s%s" % (page.parent.slug,url)
            page = page.parent
        return url
    
    def get_absolute_url(self):
        return self.parental_path()

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])
        
    def save(self, *args, **kwargs):
        if self.parent and self.parent.id == self.id:
            # raise ValidationError('You can\'t have yourself as a parent!')
            self.parent = None
        return super(StaticPage, self).save(*args, **kwargs)


class Category(SlugMixin):

    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children', on_delete=models.CASCADE
    )

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
     
        if self.published_at:
            local_publish = localtime(self.published_at)
            return reverse('blog:posts_detail',  kwargs={
                        'year': local_publish.year, 
                        'month': local_publish.month, 
                        'day': local_publish.day, 
                        'slug' :self.slug 
                        }
                    )
        return reverse('blog:posts_detail_by_id',  kwargs={'pk': self.pk })

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