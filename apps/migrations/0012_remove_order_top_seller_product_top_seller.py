# Generated by Django 4.2.13 on 2024-08-08 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0011_order_top_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='top_seller',
        ),
        migrations.AddField(
            model_name='product',
            name='top_seller',
            field=models.BooleanField(default=False),
        ),
    ]
