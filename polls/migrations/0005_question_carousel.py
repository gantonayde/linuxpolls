# Generated by Django 3.0.5 on 2020-07-10 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_question_on_focus'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='carousel',
            field=models.BooleanField(default=False),
        ),
    ]
