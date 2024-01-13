from modeltranslation.translator import TranslationOptions, translator

from shop.models import Category, Product, Tag, ProductFilter, ProductIngredient, AdditionalInfo


class NameTranslationOptions(TranslationOptions):
	fields = ('name',)


class TitleTextTranslationOptions(TranslationOptions):
	fields = ('title','text')


class ProductTranslationOptions(TranslationOptions):
	fields = ('name',)


class CategoryTranslationOptions(TranslationOptions):
	fields = ('name',)


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(Tag, NameTranslationOptions)
translator.register(ProductFilter, NameTranslationOptions)
translator.register(ProductIngredient, NameTranslationOptions)
translator.register(AdditionalInfo, TitleTextTranslationOptions)
