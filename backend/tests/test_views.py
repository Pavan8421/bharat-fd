import pytest
from rest_framework import status
from rest_framework.test import APIClient
from faqs.models import FAQ  

@pytest.mark.django_db
def test_faq_list():
    # Create some FAQ instances (will be in the test database)
    FAQ.objects.create(question="What is Django?", answer="A web framework")
    FAQ.objects.create(question="What is Python?", answer="A programming language")
    
    client = APIClient()
    response = client.get('/api/faqs/')  

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert 'question' in response.data[0]

@pytest.mark.django_db
def test_faq_crud_create():
    client = APIClient()
    data = {
        "question": "What is Django?",
        "answer": "A web framework"
    }

    response = client.post('/api/faq/', data, format='json')  
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['question'] == data['question']
    assert response.data['answer'] == data['answer']

@pytest.mark.django_db
def test_faq_crud_update():
    faq = FAQ.objects.create(question="What is Python?", answer="A programming language")
    
    client = APIClient()
    data = {
        "question": "What is Python?",
        "answer": "A popular programming language"
    }

    response = client.put(f'/api/faq/{faq.id}/', data, format='json') 
    assert response.status_code == status.HTTP_200_OK
    assert response.data['answer'] == data['answer']

@pytest.mark.django_db
def test_faq_crud_delete():
    faq = FAQ.objects.create(question="What is Flask?", answer="A micro web framework")
    
    client = APIClient()
    response = client.delete(f'/api/faq/{faq.id}/')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert FAQ.objects.count() == 0
