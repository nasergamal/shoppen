# Generated by Django 4.2.6 on 2023-10-24 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0010_rename_address_address_address_alter_address_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('shipping_address', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[(0, 'Pending'), (1, 'Confirmed'), (2, 'Shipping'), (3, 'delivered')], default=0, max_length=2)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment', models.CharField(choices=[(0, 'Cash'), (1, 'Credit card')], default=0, max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered', to='main.product')),
            ],
        ),
    ]
