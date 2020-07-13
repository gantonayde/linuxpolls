# Generated by Django 3.0.5 on 2020-07-13 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IP2LocationDBUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_code', models.CharField(blank=True, default='DB3LITEBINIPV6', max_length=20, verbose_name='Database code')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False, verbose_name='Last Update Status')),
            ],
            options={
                'verbose_name': 'IP2Location database',
                'verbose_name_plural': 'IP2Location databases',
                'ordering': ['-updated_on'],
            },
        ),
    ]