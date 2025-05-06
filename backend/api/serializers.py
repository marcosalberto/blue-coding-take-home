from rest_framework import serializers
from collections import defaultdict
from .models import (
    EHRSystem, EHRFieldMapping,
    QuestionField, QuestionAnswer,
    Form, FormAnwser, EHRIntegrationRecord
)
from .tasks import send_ehr_payload

class EHRSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EHRSystem
        fields = '__all__'

class EHRFieldMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EHRFieldMapping
        fields = '__all__'

class QuestionFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionField
        fields = '__all__'

class QuestionFieldUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionField
        fields = ['id', 'question']

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):
    fields = QuestionFieldUserSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ['id', 'name', 'fields', 'created_at', 'updated_at']

class AnswerInputSerializer(serializers.Serializer):
    questionId = serializers.IntegerField()
    value = serializers.CharField(max_length=100)

    def validate_questionId(self, value):
        if not QuestionField.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid question ID.")
        return value

class FormAnwserSerializer(serializers.ModelSerializer):
    answers = AnswerInputSerializer(many=True, write_only=True)
    created_answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='answers')
    
    class Meta:
        model = FormAnwser
        fields = ['id', 'form', 'answers', 'created_answers', 'created_at', 'updated_at']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        form_answer = FormAnwser.objects.create(**validated_data)

        ehr_payloads = defaultdict(list)

        for item in answers_data:
            question = QuestionField.objects.get(id=item['questionId'])
            answer = QuestionAnswer.objects.create(question=question, value=item['value'])
            form_answer.answers.add(answer)

            for field in question.field_mapping.all():
                ehr_payloads[field.system.name].append({
                    "key": field.field_key,
                    "value": answer.value
                })

        for system, answers in ehr_payloads.items():
            system_obj = EHRSystem.objects.get(name=system)
            if system_obj.destination_url:
                payload = {
                    "form_id": form_answer.form.id,
                    "form_name": form_answer.form.name,
                    "answers": answers
                }
                log = EHRIntegrationRecord.objects.create(
                    system=system_obj,
                    form_answer=form_answer,
                    payload=payload,
                )
                send_ehr_payload.delay(log.id)

        return form_answer