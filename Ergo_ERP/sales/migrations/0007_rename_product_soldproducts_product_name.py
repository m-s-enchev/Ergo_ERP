# Generated by Django 4.2.7 on 2023-12-29 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_alter_salesdocument_seller_representative'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soldproducts',
            old_name='product',
            new_name='product_name',
        ),
    ]
