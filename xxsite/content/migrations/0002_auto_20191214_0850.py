# Generated by Django 2.2.6 on 2019-12-14 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexcontent',
            name='content_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (3, '最新文章')], default=1, verbose_name='展示类型'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='sidebar_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (3, '最新文章')], default=1, verbose_name='展示类型'),
        ),
    ]
