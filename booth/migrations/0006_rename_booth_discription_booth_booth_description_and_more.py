# Generated by Django 5.1.6 on 2025-02-22 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0005_alter_day_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booth',
            old_name='booth_discription',
            new_name='booth_description',
        ),
        migrations.RenameField(
            model_name='booth',
            old_name='club_discription',
            new_name='club_description',
        ),
        migrations.RenameField(
            model_name='foodtruck',
            old_name='food_truck_discription',
            new_name='food_truck_description',
        ),
    ]
