# Generated by Django 4.0.3 on 2022-05-14 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_biddingsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biddingsmodel',
            name='order_id',
            field=models.CharField(max_length=15),
        ),
    ]
