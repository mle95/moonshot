# Generated by Django 4.0.3 on 2022-05-09 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_customermodel_warnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customermodel',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]