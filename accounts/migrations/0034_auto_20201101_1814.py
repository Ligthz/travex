# Generated by Django 3.1.2 on 2020-11-01 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0033_auto_20201031_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='bank_account',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
