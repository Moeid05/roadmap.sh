# Generated by Django 5.1.4 on 2025-02-19 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quentity',
            new_name='quantity',
        ),
    ]
