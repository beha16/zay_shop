# Generated by Django 4.2.13 on 2024-08-24 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0014_alter_basket_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
