# Generated by Django 3.0.5 on 2020-08-11 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_auto_20200811_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='carousel',
        ),
    ]
