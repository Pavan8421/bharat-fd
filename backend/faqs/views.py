from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FAQ
from .serializers import FAQSerializer

@api_view(['GET'])
def faq_list(request):
    """
    List all FAQs or filter by language using ?lang= query parameter.
    """
    lang = request.GET.get('lang', 'en')  # Default to 'en' if lang is not provided

    faqs = FAQ.objects.all()
    faq_data = []

    for faq in faqs:
        faq_dict = {
            "id": faq.id,
            "question": faq.get_translated_question(lang),
            "answer": faq.get_translated_answer(lang)
        }
        faq_data.append(faq_dict)
    return Response(faq_data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def faq_crud(request, pk=None):
    if request.method == 'GET':
        """
        Retrieve a single FAQ by id with language support.
        """
        lang = request.GET.get('lang', 'en')  # Default to 'en' if lang is not provided

        try:
            faq = FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            return Response({"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND)

        faq_data = {
            "id": faq.id,
            "question": faq.get_translated_question(lang),
            "answer": faq.get_translated_answer(lang)
        }

        return Response(faq_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        """
        Create a new FAQ.
        """
        serializer = FAQSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        """
        Update an existing FAQ.
        """
        try:
            faq = FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            return Response({"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FAQSerializer(faq, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Delete an FAQ by id.
        """
        try:
            faq = FAQ.objects.get(pk=pk)
        except FAQ.DoesNotExist:
            return Response({"error": "FAQ not found"}, status=status.HTTP_404_NOT_FOUND)

        faq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
