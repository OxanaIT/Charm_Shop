# Generated by Django 3.2.6 on 2021-08-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Order Received', 'Order Received'), ('Order Processing', 'Order Processing'), ('Order Canceled', 'Order Canceled'), ('On the way', 'On the way'), ('Order Completed', 'Order Completed')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(default='Picture not available', max_length=1000),
        ),
    ]
