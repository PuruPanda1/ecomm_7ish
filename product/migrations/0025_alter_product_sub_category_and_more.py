# Generated by Django 5.1.5 on 2025-02-22 12:07

import django.db.models.deletion
import smart_selects.db_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_product_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sub_category',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', on_delete=django.db.models.deletion.CASCADE, to='product.subcategory'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='product.category'),
        ),
    ]
