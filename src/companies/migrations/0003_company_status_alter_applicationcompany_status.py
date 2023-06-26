# Generated by Django 4.2.2 on 2023-06-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_applicationcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.CharField(blank=True, choices=[('ac', 'Active'), ('wt', 'Waiting'), ('rc', 'Recived'), ('rj', 'Rejected')], default='wt', max_length=3),
        ),
        migrations.AlterField(
            model_name='applicationcompany',
            name='status',
            field=models.CharField(blank=True, choices=[('ac', 'Active'), ('na', 'Not Active'), ('ar', 'Archive'), ('bn', 'Banned')], default='ac', max_length=3),
        ),
    ]