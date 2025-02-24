# Generated by Django 5.1.6 on 2025-02-17 21:03

import booth.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('club_name', models.CharField(max_length=50)),
                ('booth_name', models.CharField(max_length=50)),
                ('day', models.CharField(choices=[(None, ''), ('(수)', '(수)'), ('(목)', '(목)')], default='', max_length=20)),
                ('location', models.CharField(choices=[(None, ''), ('만해광장', '만해광장'), ('팔정도', '팔정도')], default='', max_length=30)),
                ('booth_num', models.IntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('club_logo', models.ImageField(blank=True, null=True, upload_to=booth.models.image_upload_path)),
                ('club_category', models.CharField(max_length=20)),
                ('club_discription', models.CharField(blank=True, max_length=250, null=True)),
                ('booth_discription', models.CharField(blank=True, max_length=250, null=True)),
                ('start_recruitment', models.DateField()),
                ('end_recruitment', models.DateField()),
                ('apply_method', models.CharField(max_length=300)),
                ('insta_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BoothImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=booth.models.image_upload_path)),
                ('booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='booth.booth')),
            ],
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='booth.booth')),
            ],
        ),
    ]
