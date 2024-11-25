# Generated by Django 5.1.3 on 2024-11-19 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='practicesession',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='practice_sessions', to='api.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movement',
            name='reference_file',
            field=models.FileField(upload_to='reference_files/'),
        ),
    ]
