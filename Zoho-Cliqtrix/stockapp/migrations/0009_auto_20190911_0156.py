# Generated by Django 2.2.5 on 2019-09-10 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0008_auto_20190910_1850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='string',
            old_name='hightlight',
            new_name='highlight',
        ),
        migrations.RenameField(
            model_name='work',
            old_name='hightlights',
            new_name='highlights',
        ),
    ]
