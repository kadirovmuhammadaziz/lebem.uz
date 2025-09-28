from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product, ProductImage, ProductSpecification


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description')


class ProductImageTranslationOptions(TranslationOptions):
    fields = ('alt_text',)


class ProductSpecificationTranslationOptions(TranslationOptions):
    fields = ('name', 'value')


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(ProductImage, ProductImageTranslationOptions)
translator.register(ProductSpecification, ProductSpecificationTranslationOptions)
