# Generated by Django 3.2 on 2021-04-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0011_remove_category_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Base cost per unit', max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsale',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Checkout cost per unit', max_digits=10),
        ),
        migrations.AlterField(
            model_name='productsale',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Checkout price per unit', max_digits=10),
        ),
    ]
