# Generated by Django 2.1.7 on 2019-08-25 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0003_auto_20190825_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
