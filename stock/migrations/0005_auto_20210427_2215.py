# Generated by Django 3.2 on 2021-04-27 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='items',
            field=models.ManyToManyField(help_text='Purchased items', null=True, to='stock.ProductSale'),
        ),
        migrations.AlterField(
            model_name='productsale',
            name='quantity',
            field=models.IntegerField(default=0, help_text='Quantity sold'),
        ),
    ]
