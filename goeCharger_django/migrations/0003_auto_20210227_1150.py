# Generated by Django 3.1.7 on 2021-02-27 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goeCharger_django', '0002_auto_20210227_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goecharger',
            name='ipAddress',
            field=models.GenericIPAddressField(),
        ),
    ]
