# Generated by Django 2.2.3 on 2020-11-15 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_phone',
            field=models.IntegerField(max_length=13, unique=True),
        ),
    ]
