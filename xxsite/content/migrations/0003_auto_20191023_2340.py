# Generated by Django 2.2.6 on 2019-10-23 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20191023_2333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indexcontent',
            old_name='sidebar_type',
            new_name='content_type',
        ),
    ]