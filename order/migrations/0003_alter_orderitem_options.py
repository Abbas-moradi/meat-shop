# Generated by Django 4.2.10 on 2024-02-16 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('created',), 'verbose_name': 'orderitem', 'verbose_name_plural': 'orderitems'},
        ),
    ]
