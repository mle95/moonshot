# Generated by Django 4.0.3 on 2022-05-15 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0017_ordermodel_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biddingsmodel',
            name='order_id',
            field=models.IntegerField(blank=True),
        ),
    ]