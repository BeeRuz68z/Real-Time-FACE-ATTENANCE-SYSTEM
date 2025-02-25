# Generated by Django 5.0.3 on 2024-03-12 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_department_delete_attendence_remove_faculty_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='branch',
            field=models.CharField(choices=[('CSE', 'CSE'), ('IT', 'IT'), ('ECE', 'ECE'), ('CHEM', 'CHEM'), ('MECH', 'MECH'), ('EEE', 'EEE')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='period',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='section',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='year',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=100, null=True),
        ),
    ]
