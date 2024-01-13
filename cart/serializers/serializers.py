from rest_framework import serializers

from shop.models import Product


class ProductCartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('image', 'id', 'name', 'weight', 'unit', 'get_price')
