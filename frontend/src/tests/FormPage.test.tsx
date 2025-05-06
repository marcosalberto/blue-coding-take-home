import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import FormPage from '../pages/FormPage';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { Provider } from '@/components/ui/provider';

beforeEach(() => {
  global.fetch = vi.fn((url) => {
    if (url.toString().includes('/api/v1/forms/1/')) {
      return Promise.resolve({
        json: () =>
          Promise.resolve({
            id: 1,
            name: 'Health Form',
            fields: [{ id: 101, question: 'Full Name' }],
          }),
      });
    }

    if (url.toString().includes('/api/v1/form-answers/')) {
      return Promise.resolve({ ok: true });
    }

    return Promise.reject('Unknown URL');
  }) as any;
});

it('renders and submits a form', async () => {
  render(
    <Provider>
        <MemoryRouter initialEntries={['/form/1']}>
        <Routes>
            <Route path="/form/:formId" element={<FormPage />} />
        </Routes>
        </MemoryRouter>
    </Provider>
  );

  await waitFor(() => {
    expect(screen.getByText('Full Name')).toBeInTheDocument();
  });

  fireEvent.change(screen.getByRole('textbox'), {
    target: { value: 'Jane Doe' },
  });

  fireEvent.click(screen.getByText('Submit'));

  await waitFor(() =>
    expect(screen.getByText('Form submitted successfully!')).toBeInTheDocument()
  );
});
