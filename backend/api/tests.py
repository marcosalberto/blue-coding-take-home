from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import EHRSystem, EHRFieldMapping, QuestionField, Form, EHRIntegrationRecord

class EHRSystemTestCase(APITestCase):
    def setUp(self):
        self.ehr_system_1 = EHRSystem.objects.create(name="Athena", description="Athena EHR system", destination_url="https://athena.example.com")
        self.ehr_system_2 = EHRSystem.objects.create(name="Allscripts", description="Allscripts EHR system", destination_url="https://allscripts.example.com")

        self.ehr_1_field_email = EHRFieldMapping.objects.create(
            field_name="Email", field_key="email", field_type="str", field_user_key=True, system=self.ehr_system_1
        )
        self.ehr_1_field_name = EHRFieldMapping.objects.create(
            field_name="Name", field_key="name", field_type="str", system=self.ehr_system_1
        )
        self.ehr_1_field_gender = EHRFieldMapping.objects.create(
            field_name="Gender", field_key="gender", field_type="str", system=self.ehr_system_1
        )
        self.ehr_1_field_dob = EHRFieldMapping.objects.create(
            field_name="Date of Birth", field_key="dob", field_type="int", system=self.ehr_system_1
        )

        self.ehr_2_field_email = EHRFieldMapping.objects.create(
            field_name="Email", field_key="p_email", field_type="str", field_user_key=True, system=self.ehr_system_2
        )
        self.ehr_2_field_name = EHRFieldMapping.objects.create(
            field_name="Name", field_key="p_name", field_type="str", system=self.ehr_system_2
        )
        self.ehr_2_field_gender = EHRFieldMapping.objects.create(
            field_name="Gender", field_key="p_gender", field_type="str", system=self.ehr_system_2
        )
        self.ehr_2_field_dob = EHRFieldMapping.objects.create(
            field_name="Date of Birth", field_key="p_dob", field_type="int", system=self.ehr_system_2
        )

        self.question_email = QuestionField.objects.create(question="What is your email address?")
        self.question_email.field_mapping.add(self.ehr_1_field_email)
        self.question_email.field_mapping.add(self.ehr_2_field_email)

        self.question_name = QuestionField.objects.create(question="What is your name?")
        self.question_name.field_mapping.add(self.ehr_1_field_name)
        self.question_name.field_mapping.add(self.ehr_2_field_name)

        self.question_gender = QuestionField.objects.create(question="What is your gender?")
        self.question_gender.field_mapping.add(self.ehr_1_field_gender)
        self.question_gender.field_mapping.add(self.ehr_2_field_gender)

        self.question_dob = QuestionField.objects.create(question="What is your Date of Birth?")
        self.question_dob.field_mapping.add(self.ehr_1_field_dob)
        self.question_dob.field_mapping.add(self.ehr_2_field_dob)

        self.form = Form.objects.create(name="Health Form")
        self.form.fields.add(self.question_email)
        self.form.fields.add(self.question_name)
        self.form.fields.add(self.question_gender)
        self.form.fields.add(self.question_dob)

    def test_create_form(self):
        url = reverse("form-list")
        response = self.client.get(url)
        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]['fields'][0]['question'], "What is your email address?")
        self.assertEqual(response_json[0]['fields'][1]['question'], "What is your name?")
        self.assertEqual(response_json[0]['fields'][2]['question'], "What is your gender?")
        self.assertEqual(response_json[0]['fields'][3]['question'], "What is your Date of Birth?")

    def test_create_form_answer(self):
        url = reverse("formanwser-list")
        payload = {
            "form": self.form.id,
            "answers": [
                {"questionId": self.question_email.id, "value": "barbaranavarro@example.com"},
                {"questionId": self.question_name.id, "value": "Barbara Navarro"},
                {"questionId": self.question_gender.id, "value": "Female"},
                {"questionId": self.question_dob.id, "value": 1982}
            ]
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["form"], self.form.id)
        self.assertEqual(len(response.data["created_answers"]), 4)

        system_1_records = EHRIntegrationRecord.objects.filter(system=self.ehr_system_1)
        self.assertEqual(system_1_records.count(), 1)
        system_1_recod = system_1_records.first()
        self.assertEqual(system_1_recod.status, 'pending')
        self.assertEqual(system_1_recod.response_status, None)
        self.assertEqual(system_1_recod.payload['answers'][0]["key"], "email")
        self.assertEqual(system_1_recod.payload['answers'][0]["value"], "barbaranavarro@example.com")
        self.assertEqual(system_1_recod.payload['answers'][1]["key"], "name")
        self.assertEqual(system_1_recod.payload['answers'][1]["value"], "Barbara Navarro")
        self.assertEqual(system_1_recod.payload['answers'][2]["key"], "gender")
        self.assertEqual(system_1_recod.payload['answers'][2]["value"], "Female")
        self.assertEqual(system_1_recod.payload['answers'][3]["key"], 'dob')
        self.assertEqual(system_1_recod.payload['answers'][3]["value"], '1982')

        system_2_records = EHRIntegrationRecord.objects.filter(system=self.ehr_system_2)
        self.assertEqual(system_2_records.count(), 1)
        system_2_recod = system_2_records.first()
        self.assertEqual(system_2_recod.status, 'pending')
        self.assertEqual(system_2_recod.response_status, None)
        self.assertEqual(system_2_recod.payload['answers'][0]["key"], "p_email")
        self.assertEqual(system_2_recod.payload['answers'][0]["value"], "barbaranavarro@example.com")
        self.assertEqual(system_2_recod.payload['answers'][1]["key"], "p_name")
        self.assertEqual(system_2_recod.payload['answers'][1]["value"], "Barbara Navarro")
        self.assertEqual(system_2_recod.payload['answers'][2]["key"], "p_gender")
        self.assertEqual(system_2_recod.payload['answers'][2]["value"], "Female")
        self.assertEqual(system_2_recod.payload['answers'][3]["key"], 'p_dob')
        self.assertEqual(system_2_recod.payload['answers'][3]["value"], '1982')
       