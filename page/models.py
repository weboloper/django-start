from django.db import models
from blog.managers import BaseEntryManager 
from django.utils.translation import gettext_lazy as _
from core.mixins import  AbstractNodeModel

# Create your models here.
class Page(AbstractNodeModel):

    parent = models.ForeignKey( "Page" , verbose_name=_("Parent"),  on_delete=models.CASCADE, null=True, blank=True)
    objects = BaseEntryManager()

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])

    def get_children(self):
        return Page.objects.filter(parent=self)
    
    @classmethod
    def get_root(cls):
        return cls.objects.get(parent=None)

    
    def get_absolute_url(self):
        full_path = [self.slug]
        k = self.parent
        while k is not None:
            full_path.append(k.slug)
            k = k.parent
        return '/' + '/'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if self.parent and self.parent.id == self.id:
            # raise ValidationError('You can\'t have yourself as a parent!')
            self.parent = None
        return super(Page, self).save(*args, **kwargs)