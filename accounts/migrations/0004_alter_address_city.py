# Generated by Django 4.2.10 on 2024-02-18 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_address_main_address_shamsi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50),
        ),
    ]