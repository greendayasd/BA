# Generated by Django 2.0 on 2018-01-01 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_version_teses_left'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='submitter',
        ),
    ]