# Generated by Django 3.2.3 on 2022-01-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_app', '0014_auto_20220104_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuemodel',
            name='name',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]