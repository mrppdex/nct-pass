# Generated by Django 2.1.4 on 2018-12-24 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nctbrowse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='pass_rate',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicle',
            name='year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
