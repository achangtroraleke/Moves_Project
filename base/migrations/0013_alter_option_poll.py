# Generated by Django 4.1.6 on 2023-03-06 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_option_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.poll'),
        ),
    ]
