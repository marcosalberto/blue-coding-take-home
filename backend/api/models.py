from django.db import models
from django.utils.translation import gettext_lazy as _

class EHRSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    destination_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class EHRFieldTypes(models.TextChoices):
    INTEGER = 'int', _('Integer')
    FLOAT = 'float', _('Float')
    STRING = 'str', _('String')
    BOOLEAN = 'bool', _('Boolean')
    DATE = 'date', _('Date')
    TIME = 'time', _('Time')
    DATETIME = 'datetime', _('DateTime')

class EHRFieldMapping(models.Model):
    field_name = models.CharField(max_length=100)
    field_key = models.CharField(max_length=100)
    field_type = models.CharField(choices=EHRFieldTypes.choices, default=EHRFieldTypes.STRING, max_length=20)
    field_user_key = models.BooleanField(default=False)
    system = models.ForeignKey(EHRSystem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.system.name} - {self.field_name}"

class QuestionField(models.Model):
    question = models.TextField()
    field_mapping = models.ManyToManyField(EHRFieldMapping)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Form(models.Model):
    name = models.CharField(max_length=100)
    fields = models.ManyToManyField(QuestionField)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class QuestionAnswer(models.Model):
    question = models.ForeignKey(QuestionField, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question.question} - {self.value}"

class FormAnwser(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    answers = models.ManyToManyField(QuestionAnswer)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form.name}"

class EHRIntegrationRecord(models.Model):
    system = models.ForeignKey(EHRSystem, on_delete=models.CASCADE)
    form_answer = models.ForeignKey(FormAnwser, on_delete=models.CASCADE)
    payload = models.JSONField()
    status = models.CharField(max_length=20, default='pending')  # pending, success, failed
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)