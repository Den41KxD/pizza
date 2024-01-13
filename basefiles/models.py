import os
from pathlib import Path

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.utils.translation import gettext as _

from basefiles.utils import generate_random_string, convert_to_webp


def image_upload_to(instance: 'AbstractProductImage', filename: str):
	upload_dir = f'product/{instance.product.id}/'

	base_filename, file_extension = os.path.splitext(filename)
	unique_filename = f'{instance.product.code}_{generate_random_string()}{file_extension}'

	return os.path.join(upload_dir, unique_filename.replace('/', '_'))


class AbstractCategory(models.Model):
	category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
								 related_name='children_categories', verbose_name=_('Category'))
	position = models.IntegerField(default=10, verbose_name=_('Position'))
	name = models.CharField(max_length=255, verbose_name=_("Name"))
	slug = models.CharField(max_length=255, unique=True)
	hide = models.BooleanField(default=False, verbose_name=_("Hide"), )
	image = models.ImageField(upload_to='category/', verbose_name=_("image"), null=True, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.__get_category_slug()
		super().save(*args, **kwargs)

	def get_category_breadcrumbs(self):
		category = self
		category_list = [category]
		while category:
			category = category.category
			if category:
				category_list.append(category)
		return category_list

	def __get_category_slug(self):
		counter = 0
		while True:
			slug = slugify(unidecode(self.__str__().replace('+', 'plus')))
			if counter != 0:
				slug = slug + f'-{counter}'
			if self.__class__.objects.filter(slug=slug).exists():
				counter += 1
				continue
			return slug


	class Meta:
		abstract = True


class AbstractProduct(models.Model):
	code = models.CharField(max_length=50, unique=True)
	slug = models.CharField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	hide = models.BooleanField(default=False)
	price = models.FloatField()

	def __str__(self):
		return self.name

	def get_random_product_code(self):
		return f'PC-P{self.id}O'

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None, check_code=True):
		if not self.slug:
			self.slug = self.__get_product_slug()

		super().save(force_insert=False, force_update=False, using=None, update_fields=None, )

		if not self.code and check_code:
			self.code = self.get_random_product_code()
			self.save(check_code=False)

	def __get_product_slug(self):
		counter = 0
		while True:
			slug = slugify(self.__str__().replace('+', 'plus'))
			if counter != 0:
				slug = slug + f'-{counter}'
			if self.__class__.objects.filter(slug=slug).exists():
				counter += 1
				continue
			return slug

	class Meta:
		abstract = True


class AbstractProductImage(models.Model):
	product = models.ForeignKey(AbstractProduct, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to=image_upload_to)
	image_thumbnails = models.FileField(upload_to=image_upload_to, null=True, blank=True)
	main_image = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.product.name}'

	def get_image_path(self) -> str:
		return f'{settings.BASE_DIR}/media/{self.image}'

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None, run_convertor=True):
		super().save(force_insert=False, force_update=False, using=None, update_fields=None)
		if run_convertor:
			self.image_thumbnails = convert_to_webp(Path(self.get_image_path()), size=(300, 300))
			self.image = convert_to_webp(Path(self.get_image_path()))
			self.save(run_convertor=False)

	class Meta:
		verbose_name = 'Картинка'
		verbose_name_plural = 'Картинки'
		abstract = True

