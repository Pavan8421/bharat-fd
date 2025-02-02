from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
import asyncio
import re
from django.core.cache import cache

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    # Store translations (These will still be saved in DB)
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


    def get_cached_translation(self, question, lang):
        """Check if the translation is cached in Redis using the question as key."""
        cache_key = f"{question}_{lang}"
        cached_translation = cache.get(cache_key)
        if cached_translation:
            return cached_translation
        return None

    def set_cached_translation(self, question, lang, translation):
        """Store the translation in Redis cache using the question as key."""
        cache_key = f"{question}_{lang}"
        cache.set(cache_key, translation, timeout=86400)  # Cache for 24 hours
        print(f"Stored in cache: {cache_key} -> {translation}")  # Debug print

    def save(self, *args, **kwargs):
        """Auto-translate the question and answer when saving."""

        # Translate and store translations in Redis if not already cached
        if not self.question_hi:
            cached_question_hi = self.get_cached_translation(self.question, 'hi')
            if cached_question_hi:
                self.question_hi = cached_question_hi
            else:
                self.question_hi = asyncio.run(self.translate_text(self.question, 'hi'))
                self.set_cached_translation(self.question, 'hi', self.question_hi)

        if not self.question_te:
            cached_question_te = self.get_cached_translation(self.question, 'te')
            if cached_question_te:
                self.question_te = cached_question_te
            else:
                self.question_te = asyncio.run(self.translate_text(self.question, 'te'))
                self.set_cached_translation(self.question, 'te', self.question_te)

        if not self.question_bn:
            cached_question_bn = self.get_cached_translation(self.question, 'bn')
            if cached_question_bn:
                self.question_bn = cached_question_bn
            else:
                self.question_bn = asyncio.run(self.translate_text(self.question, 'bn'))
                self.set_cached_translation(self.question, 'bn', self.question_bn)

        if not self.answer_hi:
            cached_answer_hi = self.get_cached_translation(self.answer, 'hi')
            if cached_answer_hi:
                self.answer_hi = cached_answer_hi
            else:
                self.answer_hi = asyncio.run(self.translate_text(self.answer, 'hi'))
                self.set_cached_translation(self.answer, 'hi', self.answer_hi)

        if not self.answer_te:
            cached_answer_te = self.get_cached_translation(self.answer, 'te')
            if cached_answer_te:
                self.answer_te = cached_answer_te
            else:
                self.answer_te = asyncio.run(self.translate_text(self.answer, 'te'))
                self.set_cached_translation(self.answer, 'te', self.answer_te)

        if not self.answer_bn:
            cached_answer_bn = self.get_cached_translation(self.answer, 'bn')
            if cached_answer_bn:
                self.answer_bn = cached_answer_bn
            else:
                self.answer_bn = asyncio.run(self.translate_text(self.answer, 'bn'))
                self.set_cached_translation(self.answer, 'bn', self.answer_bn)

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