# Generated by Django 4.0.3 on 2022-05-11 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_customermodel_delivery_free_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customermodel',
            name='delivery_free',
        ),
        migrations.AddField(
            model_name='customermodel',
            name='delivery_fee',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customermodel',
            name='total_spending',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='customermodel',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]