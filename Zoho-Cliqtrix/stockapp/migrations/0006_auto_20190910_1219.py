# Generated by Django 2.2.5 on 2019-09-10 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0005_auto_20190910_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='url',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='url',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='publications',
            name='website',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='website',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='work',
            name='website',
            field=models.TextField(),
        ),
    ]
