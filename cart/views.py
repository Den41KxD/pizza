from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from cart.serializers.serializers import ProductCartSerializer
from shop.models import Product


class Cart:

	def __init__(self, request):
		"""
		Инициализируем корзину
		"""
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product: Product, quantity=1, update_quantity=False):
		"""
		Добавить продукт в корзину или обновить его количество.
		"""
		new_product = False
		product_id = str(product.id)
		if product_id not in self.cart:
			new_product = True
			self.cart[product_id] = {'quantity': 0,
									 'price': str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()
		return new_product

	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True

	def remove(self, product: Product):
		"""
		Удаление товара из корзины.
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		"""
		Перебор элементов в корзине и получение продуктов из базы данных.
		"""
		product_ids = self.cart.keys()
		# получение объектов product и добавление их в корзину
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = ProductCartSerializer(product).data

		for item in self.cart.values():
			item['price'] = float(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		"""
		Подсчет всех товаров в корзине.
		"""
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		"""
		Подсчет стоимости товаров в корзине.
		"""
		return int(sum(float(item['price']) * item['quantity'] for item in self.cart.values()))

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True

	def subtract(self, product: Product, quantity=1):
		product_id = str(product.id)
		if product_id not in self.cart:
			return

		self.cart[product_id]['quantity'] -= quantity
		self.save()


def add_products_to_cart_view(request):
	cart = Cart(request)
	product = Product.objects.get(id=request.POST.get('product_id'))
	new_product = cart.add(product)
	cart_product_info = None
	if new_product:
		cart_product_info = cart.cart[str(product.id)]
		cart_product_info['product'] = ProductCartSerializer(product).data

	return JsonResponse({'total_price': cart.get_total_price(), 'products_count': len(cart), 'new_item': cart_product_info}, status=200, safe=False)


def remove_products_from_cart_view(request):
	cart = Cart(request)
	product = Product.objects.get(id=request.POST.get('product_id'))
	cart.remove(product)
	return JsonResponse({'total_price': cart.get_total_price(), 'products_count': len(cart)}, status=200, safe=False)


def subtract_products_to_cart_view(request):
	cart = Cart(request)
	product = Product.objects.get(id=request.POST.get('product_id'))
	cart.subtract(product)
	return JsonResponse({'total_price': cart.get_total_price(), 'products_count': len(cart)}, status=200, safe=False)

