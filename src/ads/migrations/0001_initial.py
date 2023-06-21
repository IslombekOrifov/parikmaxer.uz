# Generated by Django 4.2.2 on 2023-06-20 10:47

import ads.services
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=ads.services.upload_ads_path)),
                ('status', models.CharField(choices=[('ac', 'Active'), ('wt', 'Waiting'), ('na', 'Not Active'), ('ar', 'Archive'), ('bn', 'Banned')], default='wt', max_length=3)),
                ('start_at', models.DateField(auto_now=True)),
                ('end_at', models.DateField(auto_now=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ads', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='companies.company')),
            ],
        ),
    ]
