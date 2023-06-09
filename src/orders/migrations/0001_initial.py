# Generated by Django 4.2.2 on 2023-06-20 10:47

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
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ac', 'Active'), ('wt', 'Waiting'), ('rc', 'Recived'), ('rj', 'Rejected')], default='wt', max_length=2)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('company_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='companies.companybranch')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='companies.companyservice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='companies.companyworker')),
            ],
        ),
    ]
