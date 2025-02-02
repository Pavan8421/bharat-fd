from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
import asyncio
import re 

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

    def remove_html_tags(self, text):
        """Helper function to remove HTML tags from the translated text."""
        clean_text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
        return clean_text

    def save(self, *args, **kwargs):
        """Auto-translate the question and answer when saving."""

        # Use asyncio.run() to ensure an event loop is created and used
        if not self.question_hi:
            self.question_hi = asyncio.run(self.translate_text(self.question, 'hi'))
        if not self.question_te:
            self.question_te = asyncio.run(self.translate_text(self.question, 'te'))
        if not self.question_bn:
            self.question_bn = asyncio.run(self.translate_text(self.question, 'bn'))

        if not self.answer_hi:
            self.answer_hi = asyncio.run(self.translate_text(self.answer, 'hi'))
        if not self.answer_te:
            self.answer_te = asyncio.run(self.translate_text(self.answer, 'te'))
        if not self.answer_bn:
            self.answer_bn = asyncio.run(self.translate_text(self.answer, 'bn'))

        self.answer_hi = self.remove_html_tags(self.answer_hi)
        self.answer_te = self.remove_html_tags(self.answer_te)
        self.answer_bn = self.remove_html_tags(self.answer_bn)

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
