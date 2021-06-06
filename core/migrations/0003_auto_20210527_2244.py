# Generated by Django 3.2.3 on 2021-05-27 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20210527_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='lots', to=settings.AUTH_USER_MODEL, verbose_name='Owner of lot'),
        ),
        migrations.AlterField(
            model_name='lot',
            name='pet',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='lots', to='core.pet', verbose_name='Pet'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='lot',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='core.lot', verbose_name='For what lot?'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rates', to=settings.AUTH_USER_MODEL, verbose_name='Owner of rate'),
        ),
    ]
