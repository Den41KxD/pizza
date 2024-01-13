# Generated by Django 4.2.4 on 2023-09-16 20:31

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('text', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Основной Текст')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='additional_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.additionalinfo', verbose_name='Additional info'),
        ),
    ]
