import random

import factory
from shop.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Category

	name = factory.Faker('word')  # Используется случайное имя
	name_ua = factory.Faker('word')  # Используется случайное имя
	position = factory.Sequence(lambda n: n)  # Уникальная позиция для каждой категории
	hide = False
	image = factory.django.ImageField(filename='category/im_monitory-dell-6-1.webp')  # Укажите свой путь к изображениям


class ProductFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Product

	name = factory.Faker('word')
	name_ua = factory.Faker('word')
	price = factory.Faker('pyfloat', positive=True)
	category = factory.LazyFunction(lambda: random.choice([x for x in Category.objects.all() if not x.is_has_children()]))


def create_categories():
	for _ in range(10):
		CategoryFactory()


def create_products():
	for _ in range(10):
		ProductFactory()