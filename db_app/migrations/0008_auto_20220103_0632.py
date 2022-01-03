# Generated by Django 3.2.3 on 2022-01-03 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('db_app', '0007_alter_workspacemodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffworkspacemodel',
            name='staff',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staffworkspacemodel',
            name='worskspace',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='db_app.workspacemodel'),
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='staff_workspace',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db_app.staffworkspacemodel'),
        ),
    ]
