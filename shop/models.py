from django.db import models
from django.utils.translation import gettext as _
from basefiles.models import AbstractCategory, AbstractProduct, AbstractProductImage
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField

UNIT_CHOICES = (
	('g', _('grams')),
	('ml', _('milliliters'))
)


class Category(AbstractCategory):

	def preview_image(self):
		return 'http://127.0.0.1:8000/static/images/20211123202045_366bb8053.jpg'

	def is_has_children(self):
		return self.children_categories.exists()

	def get_category_products(self):
		if self.is_has_children():
			return Product.objects.filter(category__in=self.children_categories.exclude(hide=True)).exclude(
				hide=True).order_by('price')
		return self.category_products.exclude(hide=True).order_by('price')

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')


class Tag(models.Model):
	name = models.CharField(max_length=15, verbose_name=_('Name'))
	background_color = ColorField(default='#FFF')
	text_color = ColorField(default='#000')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Tag')
		verbose_name_plural = _('Tags')


class Label(models.Model):
	name = models.CharField(max_length=15, verbose_name=_('Name'))
	image = models.FileField(upload_to='labels')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Label')
		verbose_name_plural = _('Labels')


class ProductFilter(models.Model):
	name = models.CharField(max_length=50, verbose_name=_('Name'))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Filter')
		verbose_name_plural = _('Filters')


class ProductIngredient(models.Model):
	image = models.ImageField(upload_to='ingredient')
	name = models.CharField(max_length=32, verbose_name=_('Назва'))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Ingredient'
		verbose_name_plural = 'Ingredients'


class Product(AbstractProduct):
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('Category'),
								 related_name='category_products')
	tags = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
	labels = models.ManyToManyField(Label, verbose_name=_('Labels'), blank=True)
	filters = models.ManyToManyField(ProductFilter, verbose_name=_('Filters'), blank=True)
	ingredients = models.ManyToManyField(ProductIngredient, verbose_name=_('Ingredients'), blank=True)
	weight = models.IntegerField(verbose_name=_('Weight'), default=0, null=True, blank=True)
	size = models.IntegerField(verbose_name=_('Size'), null=True, blank=True)
	buy_together = models.ManyToManyField('self', verbose_name=_('Buy Together'), blank=True)
	unit = models.CharField(verbose_name=_('Unit'), choices=UNIT_CHOICES, default='g', max_length=10)
	additional_info = models.ForeignKey('AdditionalInfo', verbose_name=_('Additional info'), blank=True, null=True,
										on_delete=models.SET_NULL)

	def image(self):
		if self.product_images.exists():
			return self.product_images.filter(preview_image=True).first().image.url
		return '/static/images/default_image.webp'

	def product_page_image(self):
		if self.product_images.exists():
			return self.product_images.filter(main_image=True).first().image.url
		return '/static/images/default_image.webp'

	@property
	def get_price(self):
		return int(self.price)

	def get_buy_together_products(self):
		return self.buy_together.filter(hide=False)

	class Meta:
		verbose_name = _('Product')
		verbose_name_plural = _('Products')


class ProductImage(AbstractProductImage):
	preview_image = models.BooleanField(default=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

	class Meta:
		verbose_name = _('Image')
		verbose_name_plural = _('Images')


class ProductLink(models.Model):
	main_product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name=_('Main product'),
										related_name='linked_product')
	linked_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Linked product'),
									   related_name='main_product')
	main_product_card_text = models.CharField(max_length=10)
	linked_product_card_text = models.CharField(max_length=10)

	def __str__(self):
		return self.main_product.name

	class Meta:
		verbose_name = _('Link Product')
		verbose_name_plural = _('Link Products')


class AdditionalInfo(models.Model):
	title = models.CharField(max_length=30, verbose_name=_('Title'))
	text = RichTextField(verbose_name='Основной Текст', blank=True, null=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = _('Additional Info')
		verbose_name_plural = _('Additional Infos')
