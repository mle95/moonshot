# Generated by Django 4.0.3 on 2022-05-08 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_customermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermodel',
            name='warnings',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
