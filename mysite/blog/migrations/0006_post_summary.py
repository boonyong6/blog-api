# Generated by Django 5.0.9 on 2024-11-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_trigram_ext'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.TextField(default=''),
        ),
    ]
