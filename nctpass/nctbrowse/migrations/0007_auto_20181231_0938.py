# Generated by Django 2.1.4 on 2018-12-31 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nctbrowse', '0006_auto_20181231_0842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='pass_rate',
            new_name='passed',
        ),
    ]
