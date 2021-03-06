# Generated by Django 4.0.4 on 2022-05-17 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0026_alter_customermodel_blacklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermodel',
            name='delivery_fee',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='delivery_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
