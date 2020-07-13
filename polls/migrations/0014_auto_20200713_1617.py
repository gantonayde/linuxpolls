# Generated by Django 3.0.5 on 2020-07-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20200713_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='IP2LocationDBUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Database code')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False, verbose_name='Update Status')),
            ],
            options={
                'verbose_name': 'IP2Location database',
                'verbose_name_plural': 'IP2Location databases',
                'ordering': ['-updated_on'],
            },
        ),
        migrations.DeleteModel(
            name='DBUpdate',
        ),
    ]
