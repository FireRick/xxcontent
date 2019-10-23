# Generated by Django 2.2.6 on 2019-10-23 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20191023_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexcontent',
            name='does_show_title',
            field=models.BooleanField(default=True, verbose_name='是否显示标题'),
        ),
        migrations.AddField(
            model_name='sidebar',
            name='does_show_title',
            field=models.BooleanField(default=True, verbose_name='是否显示标题'),
        ),
        migrations.AlterField(
            model_name='indexcontent',
            name='title',
            field=models.CharField(help_text='不填则不显示标题', max_length=50, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='title',
            field=models.CharField(help_text='不填则不显示标题', max_length=50, verbose_name='标题'),
        ),
    ]
