# Generated by Django 3.1.7 on 2021-02-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goeCharger_django', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='power_max',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='power_min',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='goecharger',
            name='power_max',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='goecharger',
            name='power_min',
            field=models.IntegerField(),
        ),
    ]
