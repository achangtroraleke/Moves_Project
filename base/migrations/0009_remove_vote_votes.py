# Generated by Django 4.1.6 on 2023-03-06 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_vote_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='votes',
        ),
    ]
