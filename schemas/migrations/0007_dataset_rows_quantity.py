# Generated by Django 3.2.13 on 2022-06-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemas', '0006_auto_20220604_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='rows_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
