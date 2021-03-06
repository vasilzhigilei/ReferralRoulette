# Generated by Django 3.1.4 on 2021-01-24 03:10

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('referralroulette', '0004_auto_20210121_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemodel',
            name='company_description',
            field=tinymce.models.HTMLField(verbose_name='Company Description'),
        ),
        migrations.AlterField(
            model_name='servicemodel',
            name='referral_description',
            field=tinymce.models.HTMLField(verbose_name='Referral Description'),
        ),
    ]
