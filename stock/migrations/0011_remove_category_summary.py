# Generated by Django 3.2 on 2021-04-30 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_category_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='summary',
        ),
    ]
