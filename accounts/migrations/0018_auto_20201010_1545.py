# Generated by Django 3.1.1 on 2020-10-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_machinedata_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinedata',
            name='Value',
            field=models.CharField(default=0, max_length=10),
        ),
    ]