# Generated by Django 3.1.5 on 2021-01-16 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=256, verbose_name='URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated on')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('publish', 'Published'), ('trash', 'Trash')], default='publish', help_text='With Draft chosen, will only be shown for admin users on the site.', max_length=20, verbose_name='Status')),
                ('published_at', models.DateTimeField(blank=True, db_index=True, help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from')),
                ('expired_at', models.DateTimeField(blank=True, db_index=True, help_text="With Expired chosen, won't be shown after this time", null=True, verbose_name='Expires At')),
                ('featured_at', models.DateTimeField(blank=True, db_index=True, help_text='With Featured chosen, will set featured from this time', null=True, verbose_name='Featured at')),
                ('content', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Content body')),
                ('excerpt', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Excerpt')),
                ('node_type', models.CharField(choices=[('post', 'Blog Post'), ('news', 'News Post')], db_index=True, default='post', help_text='Node type that will be used.', max_length=20, verbose_name='Node Type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=256, verbose_name='URL')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated on')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('publish', 'Published'), ('trash', 'Trash')], default='publish', help_text='With Draft chosen, will only be shown for admin users on the site.', max_length=20, verbose_name='Status')),
                ('published_at', models.DateTimeField(blank=True, db_index=True, help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from')),
                ('expired_at', models.DateTimeField(blank=True, db_index=True, help_text="With Expired chosen, won't be shown after this time", null=True, verbose_name='Expires At')),
                ('featured_at', models.DateTimeField(blank=True, db_index=True, help_text='With Featured chosen, will set featured from this time', null=True, verbose_name='Featured at')),
                ('content', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Content body')),
                ('excerpt', models.TextField(blank=True, max_length=1500, null=True, verbose_name='Excerpt')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='blog_staticpage_created_related', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('featured_image', models.ForeignKey(blank=True, db_column='object_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.attachment', verbose_name='featured_image')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.staticpage', verbose_name='Parent')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_staticpage_updated_related', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50, verbose_name='name')),
                ('user_email', models.EmailField(max_length=254, verbose_name='email address')),
                ('user_url', models.URLField(blank=True, verbose_name='homepage')),
                ('comment', models.TextField(max_length=500, verbose_name='comment')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='ip address')),
                ('useragent', models.CharField(blank=True, max_length=100, null=True, verbose_name='user agent string')),
                ('is_public', models.BooleanField(default=True, verbose_name='is public')),
                ('is_notice', models.BooleanField(default=True, verbose_name='receive email notify')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated on')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='blog.baseentry')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.comment')),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('slug', models.SlugField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=256, verbose_name='URL')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='baseentry',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='blog_baseentry_entries', to='blog.Category'),
        ),
        migrations.AddField(
            model_name='baseentry',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='blog_baseentry_created_related', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='baseentry',
            name='featured_image',
            field=models.ForeignKey(blank=True, db_column='object_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.attachment', verbose_name='featured_image'),
        ),
        migrations.AddField(
            model_name='baseentry',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='posts', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='baseentry',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_baseentry_updated_related', to=settings.AUTH_USER_MODEL, verbose_name='Updated by'),
        ),
        migrations.CreateModel(
            name='NewsEntry',
            fields=[
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blog.baseentry',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Posts',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('blog.baseentry',),
        ),
    ]
