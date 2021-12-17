# Generated by Django 4.0 on 2021-12-17 23:25

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_alter_blog_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='', max_length=255, null=True, verbose_name='image'),
        ),
    ]