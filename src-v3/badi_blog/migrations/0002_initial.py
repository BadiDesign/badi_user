# Generated by Django 3.2.4 on 2024-07-18 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('badi_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='badi_blog.blogpost', verbose_name='خبر'),
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='replay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='badi_blog.blogcomment', verbose_name='پاسخ به'),
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='writer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='badi_blog.blogcategory', verbose_name='زیرمجموعه'),
        ),
    ]