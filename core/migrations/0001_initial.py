# Generated by Django 3.2.3 on 2021-05-27 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Price of lot')),
                ('status', models.SmallIntegerField(choices=[(1, 'active'), (2, 'closed'), (3, 'inactive')], default=1, verbose_name='Status of the lot')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lots', to=settings.AUTH_USER_MODEL, verbose_name='Owner of lot')),
            ],
            options={
                'verbose_name': 'Lot',
                'verbose_name_plural': 'Lots',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(verbose_name='Value of rate')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='core.lot', verbose_name='For what lot?')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to=settings.AUTH_USER_MODEL, verbose_name='Owner of rate')),
            ],
            options={
                'verbose_name': 'Rate',
                'verbose_name_plural': 'Rates',
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Pet's name")),
                ('breed', models.CharField(max_length=100, verbose_name='Pet breed')),
                ('kind', models.SmallIntegerField(choices=[(1, 'cat'), (2, 'hedgehog')], default=1, verbose_name='Kinds of pet')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to=settings.AUTH_USER_MODEL, verbose_name='Owner of pet')),
            ],
            options={
                'verbose_name': 'Pet',
                'verbose_name_plural': 'Pets',
            },
        ),
        migrations.AddField(
            model_name='lot',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lots', to='core.pet', verbose_name='Pet'),
        ),
    ]
