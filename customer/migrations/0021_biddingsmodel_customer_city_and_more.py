# Generated by Django 4.0.3 on 2022-05-15 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_biddingsmodel_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_state',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_street',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='customer_zip_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='biddingsmodel',
            name='home_delivery_completed',
            field=models.BooleanField(default=False),
        ),
    ]