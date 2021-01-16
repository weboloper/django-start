# Generated by Django 3.1.5 on 2021-01-16 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
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
    ]
