# Generated by Django 4.0 on 2021-12-14 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_social_medium_profile_social_facebook_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default='Earth, Milky Way', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='short_intro',
            field=models.CharField(default='BTW, I never wrote an intro BD', max_length=300),
        ),
    ]
