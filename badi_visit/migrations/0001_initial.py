# Generated by Django 3.2.4 on 2024-08-10 08:30

import badi_utils.dynamic_models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('visits_count', models.IntegerField(default=0, verbose_name='Visits count')),
                ('visitors_count', models.IntegerField(default=0, verbose_name='Visitors count')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'Address Visit',
                'verbose_name_plural': 'Address Visits',
                'ordering': ('-visitors_count',),
                'permissions': (),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=120)),
                ('model_pk', models.IntegerField(default=0)),
                ('ip', models.CharField(max_length=200, verbose_name='ip')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Visit Time')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
                'ordering': ['-pk'],
                'permissions': (('can_like', 'Manage Like'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='RedirectUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_url', models.TextField(blank=True)),
                ('to_url', models.TextField(blank=True)),
                ('is_regax', models.BooleanField(blank=True, default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'RedirectUrl',
                'verbose_name_plural': 'RedirectUrls',
                'ordering': ['-pk'],
                'permissions': (('can_redirect', 'Manage Redirects'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=250)),
                ('ip', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'SearchQuery',
                'verbose_name_plural': 'SearchQueries',
                'ordering': ['-pk'],
                'permissions': (('can_searchquery', 'Manage SearchQuery'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=200, verbose_name='ip')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Visit Time')),
                ('address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='badi_visit.addressvisit', verbose_name='Address')),
            ],
            options={
                'verbose_name': 'Visit',
                'verbose_name_plural': 'Visits',
                'ordering': ['-pk'],
                'permissions': (('can_visit', 'Manage Visit'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
    ]
