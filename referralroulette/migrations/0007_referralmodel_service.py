# Generated by Django 3.1.4 on 2020-12-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referralroulette', '0006_auto_20201223_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralmodel',
            name='service',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]