# Generated by Django 5.0.3 on 2024-03-12 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('section', models.CharField(max_length=50)),
                ('period', models.IntegerField()),
            ],
        ),
    ]
