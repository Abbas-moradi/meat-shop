# Generated by Django 4.2.10 on 2024-03-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_category_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='shamsi',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
