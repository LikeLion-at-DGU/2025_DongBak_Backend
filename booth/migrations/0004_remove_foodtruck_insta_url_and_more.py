# Generated by Django 5.1.6 on 2025-03-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0003_foodtruck_booth_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodtruck',
            name='insta_url',
        ),
        migrations.AlterField(
            model_name='foodtruck',
            name='food_truck_description',
            field=models.TextField(),
        ),
    ]
