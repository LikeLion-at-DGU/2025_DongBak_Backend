# Generated by Django 5.1.6 on 2025-02-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booth',
            name='apply_method',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='booth',
            name='booth_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booth',
            name='insta_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
