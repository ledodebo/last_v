# Generated by Django 4.2.7 on 2024-06-07 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0072_delete_test_order_date'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.productvariation'),
        ),
    ]
