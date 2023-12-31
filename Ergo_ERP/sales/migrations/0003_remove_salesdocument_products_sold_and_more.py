# Generated by Django 4.2.7 on 2023-12-28 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_salesdocument_payment_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesdocument',
            name='products_sold',
        ),
        migrations.AddField(
            model_name='soldproducts',
            name='sales_document',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='sales.salesdocument'),
            preserve_default=False,
        ),
    ]