# Generated by Django 3.1 on 2020-11-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20201109_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentaccident',
            name='only_incident',
            field=models.CharField(blank=True, choices=[('1', 'Incidente'), ('2', 'Accidente')], max_length=1),
        ),
    ]