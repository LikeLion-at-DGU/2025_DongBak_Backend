# Generated by Django 5.1.6 on 2025-02-22 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0006_rename_booth_discription_booth_booth_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booth',
            name='day',
        ),
        migrations.RemoveField(
            model_name='foodtruck',
            name='day',
        ),
        migrations.AddField(
            model_name='day',
            name='booths',
            field=models.ManyToManyField(to='booth.booth'),
        ),
    ]
