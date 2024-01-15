# Generated by Django 4.2.7 on 2024-01-13 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_invoicedata_invoice_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdocument',
            name='buyer_name',
            field=models.CharField(default='gosho', max_length=100, verbose_name='Client'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salesdocument',
            name='client_group',
            field=models.CharField(default='redovni', max_length=100, verbose_name='Client group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salesdocument',
            name='date',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='InvoicedProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoiced_product_name', models.CharField(max_length=200, verbose_name='Name')),
                ('invoiced_product_quantity', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Qty')),
                ('invoiced_product_price_before_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price before VAT')),
                ('invoiced_product_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Price')),
                ('invoiced_product_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Discount')),
                ('invoiced_product_total_before_tax', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Amount before VAT')),
                ('invoiced_product_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Amount')),
                ('invoiced_product_lot_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='LOT')),
                ('invoiced_product_exp_date', models.DateField(blank=True, null=True, verbose_name='Exp. date')),
                ('invoice_document_in_which_included', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.invoicedata')),
            ],
        ),
    ]
