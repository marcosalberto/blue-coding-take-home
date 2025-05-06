from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import (
    EHRSystem, EHRFieldMapping,
    QuestionField, QuestionAnswer,
    Form, FormAnwser
)
from .serializers import (
    EHRSystemSerializer, EHRFieldMappingSerializer,
    QuestionFieldSerializer, QuestionAnswerSerializer,
    FormSerializer, FormAnwserSerializer
)

class EHRSystemViewSet(viewsets.ModelViewSet):
    queryset = EHRSystem.objects.all()
    serializer_class = EHRSystemSerializer

class EHRFieldMappingViewSet(viewsets.ModelViewSet):
    queryset = EHRFieldMapping.objects.all()
    serializer_class = EHRFieldMappingSerializer

class QuestionFieldViewSet(viewsets.ModelViewSet):
    queryset = QuestionField.objects.all()
    serializer_class = QuestionFieldSerializer

class QuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer

@method_decorator(cache_page(60*5), name='list')
class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

class FormAnwserViewSet(viewsets.ModelViewSet):
    queryset = FormAnwser.objects.all()
    serializer_class = FormAnwserSerializer