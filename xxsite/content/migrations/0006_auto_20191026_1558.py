# Generated by Django 2.2.6 on 2019-10-26 07:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20191025_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 13, 0, 0), verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 13, 0, 0), verbose_name='更新时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 13, 0, 0), verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 13, 0, 0), verbose_name='更新时间'),
            preserve_default=False,
        ),
    ]
