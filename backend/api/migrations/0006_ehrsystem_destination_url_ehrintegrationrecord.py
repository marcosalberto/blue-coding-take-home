# Generated by Django 5.1.4 on 2025-05-06 01:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_ehrfieldmapping_field_user_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='ehrsystem',
            name='destination_url',
            field=models.URLField(blank=True),
        ),
        migrations.CreateModel(
            name='EHRIntegrationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('success', models.BooleanField(default=False)),
                ('retry_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.formanwser')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ehrsystem')),
            ],
        ),
    ]
