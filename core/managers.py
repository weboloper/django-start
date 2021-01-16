from django.db import models
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.utils import timezone


class BlogEntryManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(BlogEntryManager, self).get_queryset().filter(node_type='blog')

    def published(self):
        now = timezone.now()
        return self.get_queryset().filter(status=2).filter(published_at__lte=now)

class NewsEntryManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(NewsEntryManager, self).get_queryset().filter(node_type='news')

    def published(self):
        now = timezone.now()
        return self.get_queryset().filter(status=2).filter(published_at__lte=now)
