# Generated by Django 3.2.3 on 2021-05-29 16:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210527_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Auction end date'),
        ),
        migrations.AddField(
            model_name='lot',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Auction start date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='placement_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Rate placement date'),
            preserve_default=False,
        ),
    ]
