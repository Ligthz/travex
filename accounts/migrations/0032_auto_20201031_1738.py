# Generated by Django 3.1.2 on 2020-10-31 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0031_auto_20201031_1737'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IOTDev',
        ),
        migrations.DeleteModel(
            name='LogData',
        ),
        migrations.DeleteModel(
            name='MachineData',
        ),
    ]
