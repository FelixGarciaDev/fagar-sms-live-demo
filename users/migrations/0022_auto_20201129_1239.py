# Generated by Django 3.1 on 2020-11-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20201127_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='company',
            name='rif',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='smsmanager',
            name='phone',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
