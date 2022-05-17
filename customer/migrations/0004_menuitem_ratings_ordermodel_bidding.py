# Generated by Django 4.0.3 on 2022-05-06 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_ordermodel_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='ratings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='bidding',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
