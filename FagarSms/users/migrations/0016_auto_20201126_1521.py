# Generated by Django 3.1 on 2020-11-26 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20201112_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskreport',
            name='create_at_date',
            field=models.DateTimeField(),
        ),
    ]
