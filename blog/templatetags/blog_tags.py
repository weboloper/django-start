from django import template
from blog.models import Comment
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _
from django.utils.html import mark_safe
from hashlib import md5
import urllib
register = template.Library()

class GetCommentCountNode(Node):
    def __init__(self, entry, varname):
        self.varname = varname
        self.entry = entry
        
    def render(self, context):
        context[self.varname] = Comment.objects.filter(entry=context[self.entry],is_public=True).count()
        return ''
    
@register.tag
def get_comments_count(parser,token):
    bits = token.contents.split()
    if len(bits) < 5 or bits[3] != 'as' or bits[1] != 'for':
        raise TemplateSyntaxError
    return GetCommentCountNode(bits[2],bits[4])

class GetCommentNode(Node):
    def __init__(self, entry, varname):
        self.varname = varname
        self.entry = entry
        
    def render(self, context):
        context[self.varname] = Comment.objects.filter(entry=context[self.entry],is_public=True).order_by('created_at')
        return ''

@register.tag
def get_comments(parser,token):
    bits = token.contents.split()
    if len(bits) < 5 or bits[3] != 'as' or bits[1] != 'for':
        raise TemplateSyntaxError
    return GetCommentNode(bits[2],bits[4])

# class CommentFormNode(Node):
#     def __init__(self, varname):
#         self.varname = varname
        
#     def render(self, context):
#         context[self.varname] = CommentForm()
#         return ''

# @register.tag
# def get_comment_form(parser, token):
#     bits = token.contents.split()
#     if len(bits) < 3 or bits[1] != 'as':
#         raise TemplateSyntaxError, _("Invaild tag syntax excepted {% get_comment_form as VARNAME%}")
#     return CommentFormNode(bits[2])
 

#Refer to http://en.gravatar.com/site/implement/url
class GravatarURLNode(Node):
    GRAVATAR_URL = u'http://www.gravatar.com/avatar/%(hashed_email)s?r=%(rating)s&s=%(size)s&d=%(default)s'
    
    def __init__(self,email,size,rating,default):
        self.email = email
        self.size = size 
        self.rating = rating
        self.default = default
    
    def render(self, context):
        hashed_email = md5(self.email.resolve(context).lower()).hexdigest()
        self.url = mark_safe(self.GRAVATAR_URL % ({
            'hashed_email':hashed_email,
            'size':self.size.resolve(context),
            'rating':self.rating.resolve(context),
            'default':urllib.quote_plus(self.default)
            }))
        return self.url
    
@register.tag
def gravatar_url(parser, token):
    bits = token.contents.split()
    if len(bits) < 5:
        raise TemplateSyntaxError
    email,size,rating,default = bits[1:5]
    return GravatarURLNode(
            parser.compile_filter(email),
            parser.compile_filter(size),
            parser.compile_filter(rating),
            default)
 