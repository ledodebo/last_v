# Generated by Django 4.2.7 on 2024-05-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0050_test_info_alter_test_iteams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='iteams',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
