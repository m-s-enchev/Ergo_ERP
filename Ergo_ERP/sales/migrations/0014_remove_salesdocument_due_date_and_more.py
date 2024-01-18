# Generated by Django 4.2.7 on 2024-01-13 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_remove_salesdocument_client_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesdocument',
            name='due_date',
        ),
        migrations.AddField(
            model_name='salesdocument',
            name='is_linked_to_invoice',
            field=models.BooleanField(default=False),
        ),
    ]