# Generated by Django 5.2.3 on 2025-06-27 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azure_content', '0002_sensordata'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='luminosity',
            field=models.FloatField(default=50),
            preserve_default=False,
        ),
    ]
