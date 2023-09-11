# Generated by Django 3.2 on 2021-04-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productsale',
            options={'ordering': ['bill_id', 'product']},
        ),
        migrations.RemoveField(
            model_name='productsale',
            name='billing',
        ),
        migrations.AddField(
            model_name='productsale',
            name='bill_id',
            field=models.UUIDField(default=None, help_text='Associated bill id', null=True),
        ),
    ]
