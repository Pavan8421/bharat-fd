import pytest
from django.core.cache import cache
from faqs.models import FAQ  # Replace `myapp` with your app name
from unittest.mock import patch

@pytest.mark.django_db
def test_faq_translation_cache():
    # Create a FAQ instance
    faq = FAQ.objects.create(
        question="What is the use of Django?",
        answer="Django is a high-level Python Web framework."
    )

    # Test translation caching for 'hi' language
    faq.set_cached_translation(faq.question, 'hi', 'Django का उपयोग क्या है?')
    cached_translation = cache.get(f"{faq.question}_hi")

    assert cached_translation == 'Django का उपयोग क्या है?'
    
    # Now fetch the cached value and test if it's correctly being retrieved
    faq.question_hi = faq.get_cached_translation(faq.question, 'hi')
    assert faq.question_hi == 'Django का उपयोग क्या है?'

@pytest.mark.django_db
def test_faq_auto_translation():
    # Create a FAQ instance
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python Web framework."
    )
    
    # Test translation fields are populated after save
    assert faq.question_hi is not None
    assert faq.question_te is not None
    assert faq.question_bn is not None
    assert faq.answer_hi is not None
    assert faq.answer_te is not None
    assert faq.answer_bn is not None
