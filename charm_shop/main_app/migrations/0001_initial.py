# Generated by Django 3.2.6 on 2021-08-20 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'SubCategories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('price', models.FloatField()),
                ('return_policy', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to='products')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.category')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_by', models.CharField(max_length=200)),
                ('shipping_address', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subtotal', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('order_status', models.CharField(choices=[('Order Processing', 'Order Processing'), ('Order Received', 'Order Received'), ('On the way', 'On the way'), ('Order Canceled', 'Order Canceled'), ('Order Completed', 'Order Completed')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.customer'),
        ),
    ]
