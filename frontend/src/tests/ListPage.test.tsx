import { render, screen, waitFor } from '@testing-library/react';
import ListPage from '../pages/ListPage';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from '@/components/ui/provider'

beforeEach(() => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve([{ id: 1, name: 'Health Form' }]),
    })
  ) as any;
});

it('renders form list after loading', async () => {
  render(
    <Provider>
      <BrowserRouter>
        <ListPage />
      </BrowserRouter>
    </Provider>
  );

  expect(screen.getByRole('progressbar')).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('Health Form')).toBeInTheDocument();
  });
});