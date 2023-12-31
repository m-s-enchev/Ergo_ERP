# Generated by Django 4.2.7 on 2023-12-28 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsmodel',
            name='product_recipie_or_parts_list',
        ),
        migrations.RemoveField(
            model_name='productsmodel',
            name='product_tags',
        ),
        migrations.AddField(
            model_name='producttags',
            name='tagged_product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='products.productsmodel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productsmodel',
            name='product_type',
            field=models.CharField(choices=[('product', 'Product'), ('service', 'Service'), ('voucher', 'Voucher')], max_length=100, verbose_name='type'),
        ),
    ]
