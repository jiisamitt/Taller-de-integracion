# Generated by Django 3.2 on 2021-05-03 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareapp', '0004_auto_20210502_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='artist_id',
            field=models.CharField(blank=True, default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='track',
            name='album_id',
            field=models.CharField(blank=True, default=None, max_length=300),
        ),
    ]
