# Generated by Django 2.2.4 on 2019-08-09 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.TextField(max_length=1500),
        ),
    ]
