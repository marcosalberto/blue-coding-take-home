import React, { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Spinner, List, ListItem, Link } from '@chakra-ui/react';
import API from '@/config/API';

interface Form {
  id: number;
  name: string;
}

const FormsPage: React.FC = () => {
  const [forms, setForms] = useState<Form[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch(`${API.API_ADDRESS}/api/v1/forms/`)
      .then(res => res.json())
      .then((data: Form[]) => {
        setForms(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <Spinner role="progressbar" />;

  return (
    <List.Root>
      {forms.map(form => (
        <ListItem key={form.id}>
          <Link asChild>
            <RouterLink to={`/form/${form.id}`}>{form.name}</RouterLink>
          </Link>
        </ListItem>
      ))}
    </List.Root>
  );
};
export default FormsPage;