# Generated by Django 2.2.5 on 2019-09-09 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0004_auto_20190825_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('date', models.TextField()),
                ('awarder', models.TextField()),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Basics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('label', models.TextField()),
                ('email', models.TextField()),
                ('phone', models.TextField()),
                ('website', models.TextField()),
                ('summary', models.TextField()),
                ('address', models.TextField()),
                ('postalcode', models.TextField()),
                ('city', models.TextField()),
                ('country', models.TextField()),
                ('region', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institute', models.TextField()),
                ('area', models.TextField()),
                ('studyType', models.TextField()),
                ('startDate', models.TextField()),
                ('endDate', models.TextField()),
                ('gpa', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.TextField()),
                ('username', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Publications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('publisher', models.TextField()),
                ('releaseDate', models.TextField()),
                ('website', models.URLField()),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='References',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('reference', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('awards', models.ManyToManyField(to='stockapp.Awards')),
                ('basics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockapp.Basics')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockapp.Client')),
                ('education', models.ManyToManyField(to='stockapp.Education')),
            ],
        ),
        migrations.CreateModel(
            name='String',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hightlight', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.TextField()),
                ('position', models.TextField()),
                ('website', models.URLField()),
                ('startDate', models.TextField()),
                ('endDate', models.TextField()),
                ('summary', models.TextField()),
                ('highlights', models.ManyToManyField(to='stockapp.String')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.TextField()),
                ('position', models.TextField()),
                ('website', models.URLField()),
                ('startDate', models.TextField()),
                ('endDate', models.TextField()),
                ('summary', models.TextField()),
                ('hightlights', models.ManyToManyField(to='stockapp.String')),
            ],
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='resume',
            name='interests',
            field=models.ManyToManyField(related_name='interests', to='stockapp.String'),
        ),
        migrations.AddField(
            model_name='resume',
            name='languages',
            field=models.ManyToManyField(related_name='languages', to='stockapp.String'),
        ),
        migrations.AddField(
            model_name='resume',
            name='publications',
            field=models.ManyToManyField(to='stockapp.Publications'),
        ),
        migrations.AddField(
            model_name='resume',
            name='references',
            field=models.ManyToManyField(to='stockapp.References'),
        ),
        migrations.AddField(
            model_name='resume',
            name='skills',
            field=models.ManyToManyField(related_name='skills', to='stockapp.String'),
        ),
        migrations.AddField(
            model_name='resume',
            name='volunteer',
            field=models.ManyToManyField(to='stockapp.Volunteer'),
        ),
        migrations.AddField(
            model_name='resume',
            name='works',
            field=models.ManyToManyField(to='stockapp.Work'),
        ),
        migrations.AddField(
            model_name='education',
            name='courses',
            field=models.ManyToManyField(to='stockapp.String'),
        ),
        migrations.AddField(
            model_name='basics',
            name='profiles',
            field=models.ManyToManyField(to='stockapp.Profile'),
        ),
    ]
