from django import template
from core.models import SiteSetting 
from django.utils.translation import gettext_lazy as _

register = template.Library()

class SiteSettingContentNode(template.Node):
    def __init__(self, format_string):
        self.format_string = format_string

    def render(self, context):
        context[self.format_string] = SiteSetting.objects.get_current()
        return ''

@register.tag
def get_siteinfo(parser, token):
    bits = token.contents.split()
    
    if len(bits) < 3 or bits[1] != 'as':
        raise template.TemplateSyntaxError( _("Invaild tag syntax excepted {% get_siteinfo as VARNAME%}"))
    return SiteSettingContentNode(bits[2])

@register.simple_tag
def get_meta(self, meta_key, unique=True ):   
    return self.get_meta( meta_key, unique )

#ACL
@register.filter
def can_edit(value, arg):
    user, obj = value, arg
    if user.is_staff:
        return True
    if hasattr(obj, 'created_by'):
        return obj.created_by==user
    return False

@register.filter
def can_delete(value, arg):
    return can_edit(value, arg)

@register.simple_tag(takes_context=True)
def has_permission(context, user, permission_required):
    """
    Permite validar un permiso dentro de un template
    """
    if user.is_active is False:
        return False
    if user.is_superuser is True:
        return True
    groups = user.groups.all()
    for group in groups:
        for permission in group.permissions.all():
            if permission.codename == permission_required:
                return True
    return False


@register.simple_tag(takes_context=True)
def has_role(context, user, group_required):
    """
    Permite validar un role dentro de un template
    """
    if user.is_active is False:
        return False

    groups = user.groups.all()
    for group in groups:
        if group.name == group_required:
            return True
    return False



##
# Organizations


# @register.simple_tag(takes_context=True)
# def is_user_organization_owner(context, organization):
#     user = context.get('user', None)
#     if user:
#         is_owner = organization.has_owner(user)
#     else:
#         is_owner = False
#     return is_owner


# @register.simple_tag(takes_context=True)
# def is_user_organization_admin(context, organization):
#     user = context.get('user', None)
#     if user:
#         is_admin = organization.has_admin(user)
#     else:
#         is_admin = False
#     return is_admin


# @register.simple_tag(takes_context=True)
# def is_user_organization_member(context, organization):
#     user = context.get('user', None)
#     if user:
#         is_member = organization.has_member(user)
#     else:
#         is_member = False
#     return is_member
