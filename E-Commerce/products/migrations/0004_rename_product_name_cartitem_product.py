# Generated by Django 5.1.4 on 2025-02-28 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_quentity_cartitem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='product_name',
            new_name='product',
        ),
    ]
