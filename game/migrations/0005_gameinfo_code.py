# Generated by Django 3.2.6 on 2021-08-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_alter_gameinfo_movements'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinfo',
            name='code',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
