import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Button, Field,
  Input, Spinner, VStack
} from '@chakra-ui/react';
import { Toaster, toaster } from "@/components/ui/toaster"
import API from '@/config/API';

interface QuestionField {
  id: number;
  question: string;
}

interface Form {
  id: number;
  name: string;
  fields: QuestionField[];
}

interface AnswerPayload {
  questionId: number;
  value: string;
}

const FormPage: React.FC = () => {
  const { formId } = useParams<{ formId: string }>();
  const [form, setForm] = useState<Form | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});

  useEffect(() => {
    fetch(`${API.API_ADDRESS}/api/v1/forms/${formId}/`)
      .then(res => res.json())
      .then((data: Form) => {
        setForm(data);
      });
  }, [formId]);

  const handleChange = (questionId: number, value: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSubmit = () => {
    const payload = {
      form: form?.id,
      answers: Object.entries(answers).map(([questionId, value]) => ({
        questionId: parseInt(questionId),
        value,
      })) as AnswerPayload[]
    };

    fetch(`${API.API_ADDRESS}/api/v1/form-answers/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    .then(res => {
        if (!res.ok) throw new Error('Failed');
        toaster.create({ title: 'Form submitted successfully!', type: 'success' });
        setAnswers({})
    })
    .catch(() => {
        toaster.create({ title: 'Submission failed.', type: 'error' });
      });
  };

  if (!form) return <Spinner />;

  return (
    <VStack align="stretch">
      {form.fields.map(field => (
        <Field.Root key={field.id}>
          <Field.Label>{field.question}</Field.Label>
          <Input 
            onChange={e => handleChange(field.id, e.target.value)} 
            value={answers[field.id] || ''}
            required
          />
        </Field.Root>
      ))}
      <Button colorScheme="blue" onClick={handleSubmit}>Submit</Button>
      <Toaster />
    </VStack>
  );
};

export default FormPage;