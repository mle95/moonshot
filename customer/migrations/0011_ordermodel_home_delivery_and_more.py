# Generated by Django 4.0.3 on 2022-05-10 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_delete_user_customermodel_vip_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='home_delivery',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='home_delivery_completed',
            field=models.BooleanField(default=False),
        ),
    ]
