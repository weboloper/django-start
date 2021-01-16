import datetime
from django.core.exceptions import ObjectDoesNotExist

def upload_location(instance, filename):
    # print(instance.pk)
    # https://gist.github.com/LeoHeo/5131362006bd2ee9b693b3e29692c42f
    now = datetime.datetime.now()
    path = "{year}/{month}/{day}/{filename}".format(
        year=now.year,
        month=str(now.month).zfill(2),
        day=str(now.day).zfill(2),
        filename=filename,
    )
    return path

def unique_slug(queryset, slug_field, slug):
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit("-", 1)[0]
            slug = "%s-%s" % (slug, i)
        try:
            queryset.get(**{slug_field: slug})
        except ObjectDoesNotExist:
            break
        i += 1
    return slug
