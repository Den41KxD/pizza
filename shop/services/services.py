from typing import List

from django.db.models import QuerySet

from shop.models import Product, ProductFilter, Category


def get_product_by_id(product_id: int) -> Product:
	return Product.objects.get(id=product_id)


def get_filters_by_products(products: QuerySet['Product']) -> QuerySet['ProductFilter']:
	products = Product.objects.filter(id__in=products.values_list('id', flat=True))
	products_with_filters = products.prefetch_related('filters')
	filters_ids = []
	for product in products_with_filters:
		filters_for_product = product.filters.values_list('id', flat=True)
		filters_ids = filters_ids + [*filters_for_product]
	return ProductFilter.objects.filter(id__in=filters_ids)


def get_filtered_products(category_id: int, filter_ids: List[str]) -> QuerySet['Product']:
	products = Category.objects.get(id=category_id).get_category_products()
	if not filter_ids:
		return products

	products = products.filter(filters__id__in=filter_ids).order_by('id').distinct().order_by('price')
	return products
