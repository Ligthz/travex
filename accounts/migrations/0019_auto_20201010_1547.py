# Generated by Django 3.1.1 on 2020-10-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20201010_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinedata',
            name='Value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]