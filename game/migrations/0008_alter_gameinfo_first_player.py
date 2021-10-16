# Generated by Django 3.2.6 on 2021-10-14 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0007_auto_20210929_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameinfo',
            name='first_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='first_player', to=settings.AUTH_USER_MODEL, verbose_name='First player'),
        ),
    ]