# Generated by Django 3.1 on 2020-11-26 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20201126_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskreport',
            name='create_at_date',
            field=models.DateTimeField(),
        ),
    ]
