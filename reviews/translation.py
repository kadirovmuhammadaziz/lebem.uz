from modeltranslation.translator import translator, TranslationOptions
from .models import Review, ContactMessage


class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)


class ContactMessageTranslationOptions(TranslationOptions):
    fields = ('message',)


translator.register(Review, ReviewTranslationOptions)
translator.register(ContactMessage, ContactMessageTranslationOptions)