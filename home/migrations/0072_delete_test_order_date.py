# Generated by Django 4.2.7 on 2024-06-05 10:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0071_delete_test_order_device'),
    ]

    operations = [
      
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
