# Generated by Django 3.2.4 on 2024-08-10 08:30

import badi_utils.dynamic_models
import badi_utils.utils
import badi_utils.validations
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('picture', models.FileField(blank=True, null=True, upload_to='blog_banner/%Y/%m/%d/', verbose_name='Picture')),
                ('picture_sm', models.FileField(blank=True, null=True, upload_to='blog_banner/%Y/%m/%d/', verbose_name='Picture sm')),
                ('lang', models.CharField(blank=True, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ar-dz', 'Algerian Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dsb', 'Lower Sorbian'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hsb', 'Upper Sorbian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('ig', 'Igbo'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kab', 'Kabyle'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('ky', 'Kyrgyz'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmål'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('tk', 'Turkmen'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese')], default='fa', max_length=10, null=True)),
                ('link', models.CharField(max_length=200, verbose_name='link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'BlogBanner',
                'verbose_name_plural': 'BlogBanners',
                'ordering': ['-pk'],
                'permissions': (('can_manage_banner', 'Manage BlogBanners'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Keywords meta tag')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description meta tag')),
                ('meta_author', models.CharField(blank=True, max_length=255, null=True, verbose_name='Author meta tag')),
                ('meta_copyright', models.CharField(blank=True, max_length=255, null=True, verbose_name='Copyright meta tag')),
                ('meta_title', models.CharField(blank=True, max_length=225, null=True, verbose_name='title meta tag')),
                ('extra_header', models.TextField(blank=True, null=True, verbose_name='Extra header html')),
                ('extra_scripts', models.TextField(blank=True, null=True, verbose_name='Extra script html')),
                ('google_analytics_details', models.TextField(blank=True, null=True, verbose_name='google analytics Details')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='عنوان')),
                ('index_show', models.BooleanField(default=False, null=True, verbose_name='ترتیب')),
                ('index_order', models.IntegerField(blank=True, default=0, null=True, verbose_name='ترتیب نمایش')),
                ('title_show_type', models.CharField(blank=True, choices=[('1', 'نمایش نوع 1'), ('2', 'نمایش نوع 2'), ('3', 'نمایش نوع 3'), ('4', 'نمایش نوع 4')], max_length=2, null=True, verbose_name='چیدمان عنوان')),
                ('post_show_type', models.CharField(blank=True, choices=[('1', 'نمایش نوع 1'), ('2', 'نمایش نوع 2'), ('3', 'نمایش نوع 3'), ('4', 'نمایش نوع 4')], max_length=2, null=True, verbose_name='چیدمان پست ها')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='blog_post/%Y/%m/%d/', verbose_name='تصویر')),
                ('slug', models.CharField(blank=True, max_length=256, null=True, validators=[badi_utils.validations.BadiValidators.slug], verbose_name='متن Slug دسته بندی')),
                ('description', models.TextField(blank=True, verbose_name='شرح دسته بندی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='badi_blog.blogcategory', verbose_name='زیرمجموعه')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['index_order'],
                'permissions': (('can_category', 'مدیریت دسته بندی ها'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/', validators=[badi_utils.utils.file_size], verbose_name='کاور')),
                ('url', models.TextField(blank=True, null=True, verbose_name='url')),
                ('alt', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصویر ها',
                'ordering': ['-pk'],
                'permissions': (),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='BlogPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='blog_partner/', validators=[badi_utils.utils.file_size], verbose_name='تصویر')),
                ('name', models.CharField(max_length=200, verbose_name='نام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'همکار',
                'verbose_name_plural': 'همکاران',
                'ordering': ['-pk'],
                'permissions': (('can_blog_partner', 'مدیریت همکاران'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='عنوان')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
                'ordering': ['-pk'],
                'permissions': (('can_category', 'مدیریت تگ ها'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='Keywords meta tag')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description meta tag')),
                ('meta_author', models.CharField(blank=True, max_length=255, null=True, verbose_name='Author meta tag')),
                ('meta_copyright', models.CharField(blank=True, max_length=255, null=True, verbose_name='Copyright meta tag')),
                ('meta_title', models.CharField(blank=True, max_length=225, null=True, verbose_name='title meta tag')),
                ('extra_header', models.TextField(blank=True, null=True, verbose_name='Extra header html')),
                ('extra_scripts', models.TextField(blank=True, null=True, verbose_name='Extra script html')),
                ('google_analytics_details', models.TextField(blank=True, null=True, verbose_name='google analytics Details')),
                ('title', models.CharField(max_length=200, verbose_name='تیتر')),
                ('pre_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='پیش تیتر')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='blog_post/%Y/%m/%d/', verbose_name='تصویر')),
                ('slug', models.CharField(max_length=256, validators=[badi_utils.validations.BadiValidators.slug], verbose_name='متن Slug خبر')),
                ('slider_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='تیتر اسلایدر')),
                ('slider_picture', models.ImageField(blank=True, null=True, upload_to='blog_post/%Y/%m/%d/slider/', verbose_name='تصویر اسلایدر')),
                ('breaking_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='تیتر فوری')),
                ('is_recommend', models.BooleanField(blank=True, default=False, verbose_name='پیشنهادی')),
                ('short', models.TextField(validators=[django.core.validators.MaxLengthValidator(1200)], verbose_name='خلاصه خبر')),
                ('description', models.TextField(blank=True, verbose_name='شرح خبر')),
                ('view', models.IntegerField(default=0, verbose_name='تعداد بازدید')),
                ('source_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان منبع')),
                ('source_link', models.URLField(blank=True, null=True, verbose_name='لینک منبع')),
                ('picture_alt', models.CharField(max_length=255, null=True, verbose_name='آلت تصویر')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان آخرین ویرایش')),
                ('categories', models.ManyToManyField(related_name='news', to='badi_blog.BlogCategory', verbose_name='دسته بندی ها')),
                ('tags', models.ManyToManyField(related_name='news', to='badi_blog.BlogTag', verbose_name='تگ ها')),
                ('writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'خبر',
                'verbose_name_plural': 'اخبار',
                'ordering': ['-pk'],
                'permissions': (('can_blog_post', 'مدیریت اخبار'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(validators=[django.core.validators.MaxLengthValidator(500)], verbose_name='متن دیدگاه')),
                ('writer_name', models.CharField(blank=True, max_length=40, verbose_name='نام نویسنده')),
                ('writer_phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تماس نویسنده')),
                ('is_accepted', models.BooleanField(blank=True, default=False, verbose_name='تایید شده')),
                ('is_rejected', models.BooleanField(blank=True, default=False, verbose_name='رد شده')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='badi_blog.blogpost', verbose_name='خبر')),
                ('replay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='badi_blog.blogcomment', verbose_name='پاسخ به')),
                ('writer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظر ها',
                'ordering': ['-id'],
                'permissions': (('can_comment', 'مدیریت نظرات'),),
            },
            bases=(models.Model, badi_utils.dynamic_models.BadiModel),
        ),
    ]
