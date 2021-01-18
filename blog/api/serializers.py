from blog.models import   Post, Category
from rest_framework import routers, serializers, pagination
from taggit.models import Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'slug'


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    featured_image = serializers.SerializerMethodField("get_featured_image")

    def get_featured_image(self, post):
        request = self.context.get('request')
        if post.featured_image:
            thumbnail = post.featured_image.get_image_url(geometry = '200x200')
        
            return request.build_absolute_uri(thumbnail)
        return None
       
    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'
    
class CategoryDetailSerializer(CategorySerializer):
    # https://github.com/ydPro-G/typeidea/blob/4c4f5da9351f344c348518e4a5a60236d7683800/typeidea/typeidea/blog/serializers.py
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        # posts = obj.posts.published()
        posts = Post.objects.list_by_category( obj )
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }