# Generated by Django 5.1.5 on 2025-02-06 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_orderitem_price_remove_orderitem_tax_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_total',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price_pre_tax',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_tax',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='returns',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='returns', to='orders.orderitem'),
        ),
    ]
