# Generated by Django 2.0 on 2018-01-01 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20180101_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='teses_left',
            field=models.IntegerField(default=1),
        ),
    ]
