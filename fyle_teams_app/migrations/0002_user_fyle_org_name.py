# Generated by Django 3.2.13 on 2022-06-03 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyle_teams_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fyle_org_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
