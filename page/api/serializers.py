from page.models import Page
from rest_framework import routers, serializers, pagination
from taggit.models import Tag


class PageSerializer(serializers.ModelSerializer):
  
    featured_image = serializers.SerializerMethodField("get_featured_image")

    def get_featured_image(self, post):
        request = self.context.get('request')
        if post.featured_image:
            thumbnail = post.featured_image.get_image_url(geometry = '200x200')
        
            return request.build_absolute_uri(thumbnail)
        return None
       
    class Meta:
        model = Page
        fields = '__all__'
        lookup_field = 'slug'
    