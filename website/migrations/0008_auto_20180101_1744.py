# Generated by Django 2.0 on 2018-01-01 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_player_test2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='test',
        ),
        migrations.RemoveField(
            model_name='player',
            name='test2',
        ),
    ]