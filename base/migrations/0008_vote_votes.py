# Generated by Django 4.1.6 on 2023-03-06 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_poll_venues_poll_venues'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
