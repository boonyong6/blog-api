# Generated by Django 5.0.9 on 2024-11-22 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('link', models.URLField()),
                ('thumbnail', models.ImageField(upload_to='images/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
