# Generated by Django 3.1.1 on 2020-10-10 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20201010_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machinedata',
            name='Value',
        ),
    ]
