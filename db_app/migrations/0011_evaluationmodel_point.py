# Generated by Django 4.0 on 2022-01-03 16:48
# Generated by Django 3.2.3 on 2022-01-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0010_rename_worskspace_staffworkspacemodel_workspace'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationmodel',
            name='point',
            field=models.IntegerField(null=True),
        ),
    ]
