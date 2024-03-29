# Generated by Django 4.2.4 on 2023-09-03 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_label_productfilter_tag_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='product',
            name='filters',
            field=models.ManyToManyField(blank=True, to='shop.productfilter', verbose_name='Filters'),
        ),
        migrations.AlterField(
            model_name='product',
            name='labels',
            field=models.ManyToManyField(blank=True, to='shop.label', verbose_name='Labels'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='shop.tag', verbose_name='Tags'),
        ),
    ]
