from django.contrib import admin
from django.contrib.admin import StackedInline

from shop.models import Category, Product, ProductImage, Tag, ProductFilter, Label, ProductLink, ProductIngredient, AdditionalInfo
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
	exclude = ('slug',)


class ImageInline(StackedInline):
	model = ProductImage
	extra = 1
	exclude = ('image_thumbnails', )


class ProductAdmin(TranslationAdmin):
	exclude = ('slug', 'code')
	readonly_fields = ('slug', 'code')
	filter_horizontal = ('tags', 'labels', 'filters', 'buy_together', 'ingredients')
	inlines = [ImageInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TranslationAdmin)
admin.site.register(ProductIngredient, TranslationAdmin)
admin.site.register(ProductFilter, TranslationAdmin)
admin.site.register(AdditionalInfo, TranslationAdmin)
admin.site.register(Label, admin.ModelAdmin)
admin.site.register(ProductLink, admin.ModelAdmin)
