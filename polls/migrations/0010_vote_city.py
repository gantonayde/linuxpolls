# Generated by Django 3.0.5 on 2020-07-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20200712_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]