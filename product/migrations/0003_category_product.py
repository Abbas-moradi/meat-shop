# Generated by Django 4.2.10 on 2024-03-05 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('pic', models.ImageField(upload_to='category/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('inventory', models.PositiveIntegerField()),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('pic', models.ImageField(upload_to='product/')),
                ('discount', models.PositiveSmallIntegerField()),
                ('economic', models.BooleanField(default=False)),
                ('unit', models.CharField(choices=[('کیلوگرم', 'kg'), ('بسته', 'pk'), ('یک دست', 'st')], max_length=10)),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('created',),
            },
        ),
    ]