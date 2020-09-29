# Generated by Django 2.2 on 2020-05-21 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200520_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='iotdev',
            name='LastSeen',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='logdata',
            name='DateCreated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='machinedata',
            name='LastEdit',
            field=models.DateTimeField(null=True),
        ),
    ]
