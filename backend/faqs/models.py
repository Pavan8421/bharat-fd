from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
import asyncio
import re
from django.core.cache import cache

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    # Store translations
    question_hi = models.TextField(blank=True, null=True)
    question_te = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_hi = models.TextField(blank=True, null=True)
    answer_te = models.TextField(blank=True, null=True)
    answer_bn = models.TextField(blank=True, null=True)

    async def translate_text(self, text, dest_lang):
        """Helper function to translate text asynchronously."""
        translator = Translator()
        try:
            # Await the translation call
            translated_text = await translator.translate(text, src='en', dest=dest_lang)
            return translated_text.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def get_cached_translation(self, key):
        """Check if the translation is cached in Redis."""
        cached_translation = cache.get(key)
        if cached_translation:
            return cached_translation
        return None

    def set_cached_translation(self, key, value):
        """Store the translation in Redis cache."""
        cache.set(key, value, timeout=86400)  # Cache for 24 hours

    def save(self, *args, **kwargs):
        """Auto-translate the question and answer when saving."""

        # Translate and store translations in Redis if not already cached
        if not self.question_hi:
            cached_question_hi = self.get_cached_translation(f"{self.id}_question_hi")
            if cached_question_hi:
                self.question_hi = cached_question_hi
            else:
                self.question_hi = asyncio.run(self.translate_text(self.question, 'hi'))
                self.set_cached_translation(f"{self.id}_question_hi", self.question_hi)

        if not self.question_te:
            cached_question_te = self.get_cached_translation(f"{self.id}_question_te")
            if cached_question_te:
                self.question_te = cached_question_te
            else:
                self.question_te = asyncio.run(self.translate_text(self.question, 'te'))
                self.set_cached_translation(f"{self.id}_question_te", self.question_te)

        if not self.question_bn:
            cached_question_bn = self.get_cached_translation(f"{self.id}_question_bn")
            if cached_question_bn:
                self.question_bn = cached_question_bn
            else:
                self.question_bn = asyncio.run(self.translate_text(self.question, 'bn'))
                self.set_cached_translation(f"{self.id}_question_bn", self.question_bn)

        if not self.answer_hi:
            cached_answer_hi = self.get_cached_translation(f"{self.id}_answer_hi")
            if cached_answer_hi:
                self.answer_hi = cached_answer_hi
            else:
                self.answer_hi = asyncio.run(self.translate_text(self.answer, 'hi'))
                self.set_cached_translation(f"{self.id}_answer_hi", self.answer_hi)

        if not self.answer_te:
            cached_answer_te = self.get_cached_translation(f"{self.id}_answer_te")
            if cached_answer_te:
                self.answer_te = cached_answer_te
            else:
                self.answer_te = asyncio.run(self.translate_text(self.answer, 'te'))
                self.set_cached_translation(f"{self.id}_answer_te", self.answer_te)

        if not self.answer_bn:
            cached_answer_bn = self.get_cached_translation(f"{self.id}_answer_bn")
            if cached_answer_bn:
                self.answer_bn = cached_answer_bn
            else:
                self.answer_bn = asyncio.run(self.translate_text(self.answer, 'bn'))
                self.set_cached_translation(f"{self.id}_answer_bn", self.answer_bn)


        super().save(*args, **kwargs)

    def get_translated_question(self, lang='en'):
        """Retrieve the stored translation for the question."""
        translations = {
            'hi': self.question_hi,
            'bn': self.question_bn,
            'te': self.question_te,
        }
        return translations.get(lang, self.question)

    def get_translated_answer(self, lang='en'):
        """Retrieve the stored translation for the answer."""
        translations = {
            'hi': self.answer_hi,
            'bn': self.answer_bn,
            'te': self.answer_te,
        }
        return translations.get(lang, self.answer)

    def __str__(self):
        return self.question
