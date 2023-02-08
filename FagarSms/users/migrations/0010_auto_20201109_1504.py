# Generated by Django 3.1 on 2020-11-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_incidentaccident_only_incident'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentaccident',
            name='only_incident',
            field=models.CharField(blank=True, choices=[('1', 'Relacionado con vuelo'), ('2', 'E.P.P. (Equipos de protección personal)'), ('3', 'Procedimientos'), ('4', 'Mantenimiento Aeronáutico'), ('5', 'FOD (Objetos extraños)'), ('6', 'Orden y limpieza'), ('7', 'Acto inseguro'), ('8', 'Otros')], max_length=1),
        ),
    ]
