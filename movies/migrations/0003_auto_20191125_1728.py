# Generated by Django 2.2.7 on 2019-11-25 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20191125_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searcheddate',
            old_name='date',
            new_name='day',
        ),
    ]
