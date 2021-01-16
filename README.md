# django-start

migrate and use

## vendor apps

⋅⋅* bootstrap4
⋅⋅* tinymce
⋅⋅* taggit
⋅⋅* sorl.thumbnail
⋅⋅\* rest_framework

##template tags

`{% get_siteinfo as site %} {{ site.title }}`
`{% get_meta object 'meta_key1' %}`
`{% get_meta object 'meta_key1' False %}`
`{% get_meta object 'meta_key1' False as meta_list %}`
`{% if user|can_edit:object %}`
`{{ object.url_to_edit_object }}`
`{% has_permission request.user 'change_post' as has_permission_update %}`
`{% has_role request.user 'MODERATOR' as has_role_modarator %}`
