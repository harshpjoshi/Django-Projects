# Generated by Django 2.2.4 on 2019-08-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='totalprice',
            field=models.IntegerField(default=0),
        ),
    ]
