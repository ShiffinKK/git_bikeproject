# Generated by Django 4.2.9 on 2024-04-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0003_pricerange_alter_order_bike_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='is_placed',
            field=models.BooleanField(default=False),
        ),
    ]