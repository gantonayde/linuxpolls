# Generated by Django 3.0.5 on 2020-07-13 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_vote_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plot',
            old_name='update',
            new_name='allow_updates',
        ),
    ]
