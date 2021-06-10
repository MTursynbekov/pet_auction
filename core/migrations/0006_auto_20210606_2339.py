# Generated by Django 3.2.3 on 2021-06-06 17:39

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210531_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='is_won',
            field=models.BooleanField(default=False, verbose_name='Is bid won?'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='end_date',
            field=models.DateTimeField(blank=True, default=core.models.default_end_time, null=True, verbose_name='Auction end date'),
        ),
    ]
