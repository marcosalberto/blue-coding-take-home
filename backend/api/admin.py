from django.contrib import admin
from .models import (
    EHRSystem, EHRFieldMapping,
    QuestionField, QuestionAnswer,
    Form, FormAnwser, EHRIntegrationRecord
)

@admin.register(EHRSystem)
class EHRSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

    class Meta:
        verbose_name = 'EHR System'
        verbose_name_plural = 'EHR Systems'

@admin.register(EHRFieldMapping)
class EHRFieldMappingAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'field_key', 'system', 'created_at')
    
    class Meta:
        verbose_name = 'EHR Field Mapping'
        verbose_name_plural = 'EHR Field Mapping'

@admin.register(QuestionField)
class QuestionFieldAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
        
    class Meta:
        verbose_name = 'Question Field'
        verbose_name_plural = 'Question Fields'

@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'value', 'created_at')
        
    class Meta:
        verbose_name = 'Question Anwser'
        verbose_name_plural = 'Question Anwsers'

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
        
    class Meta:
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'

@admin.register(FormAnwser)
class FormAnwserAdmin(admin.ModelAdmin):
    list_display = ('form', 'created_at')
        
    class Meta:
        verbose_name = 'Form Answers'
        verbose_name_plural = 'Form Answers'

@admin.register(EHRIntegrationRecord)
class EHRIntegrationRecordAdmin(admin.ModelAdmin):
    list_display = ('system', 'created_at', 'status')
        
    class Meta:
        verbose_name = 'EHR Integration Record'
        verbose_name_plural = 'EHR Integration Records'