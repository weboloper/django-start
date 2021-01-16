from django.db import models
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.utils import timezone
# from blog.models import Category

class CategoryManager(models.Manager):

	def get_categories(self, number):
		return super(CategoryManager, self).get_query_set().filter(parent=number)

	def get_descendants(self, parent_id):
		ls ={}
		descs = self.get_categories(parent_id)
		
		for node in descs:
		    if node.id !=1:    
		        ls[node] = self.get_descendants(node.id)
		
		return ls

	# def get_category_items(self, list):
	# 	items = set()
	# 	for key,val in list.items():
	# 		items.update(Category.objects.filter(category_id = key.id))
	# 		if val:
	# 			items.update(self.get_category_items(val))
	# 	return items


class BaseEntryManager(models.Manager):

    def get_queryset(self):
        return super(BaseEntryManager, self).get_queryset()

    def published(self):
        now = timezone.now()
        return self.get_queryset().filter(status='publish').filter(published_at__lte=now).filter(Q(expired_at__gte=now) | Q(expired_at=None)).order_by(
        "-published_at")

    def featured(self):
        return self.published().exclude(featured_at=None).order_by(
        "featured_at")

    def list_by_category_slug(self, category_slug):
        return self.published().filter(categories__slug=category_slug)

    def list_by_category(self, category):
        return self.published().filter(categories=category)

    def create(self, **kwargs):
        kwargs.setdefault('node_type', self.model.limit_to_post_type)
        super(BaseEntryManager, self).create(**kwargs)

    def get_recent(self, count = 5 ):
        total_count = self.published().count()
        if total_count <= count:
            return self.published()
        else:
            return self.published()[:count]
    
    def get_years(self):
        dates = self.published().values_list('published_at')
        year_list = []
        archive_year = []

        for d in dates:
            if d[0].year not in year_list:
                year_list.append( d[0].year )
                posts = self.published().filter(published_at__year=d[0].year).count()
                archive_year.append( (d[0].year, posts) )

        year_list = None
        return archive_year 

    def get_months(self, year):
        dates = self.published().filter(published_at__year=year).values_list('date_published')
        month_list = []
        archive_month = []

        for d in dates:
            if d[0].month not in month_list:
                month_list.append( d[0].month )
                posts = self.published().filter(published_at__year=year).filter(published_at__month=d[0].month).count()
                archive_month.append( (d[0].month, d[0].strftime('%B'), posts) )

        month_list = None
        return archive_month



class PostManager(BaseEntryManager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(node_type='post')

class NewsEntryManager(BaseEntryManager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(NewsEntryManager, self).get_queryset().filter(node_type='news')

 
