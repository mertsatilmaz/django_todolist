# Generated by Django 2.2.1 on 2019-05-01 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-last_updated', '-created_time']},
        ),
        migrations.AlterField(
            model_name='todo',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]