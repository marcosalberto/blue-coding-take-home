import { render, screen } from '@testing-library/react'
import { Provider } from '@/components/ui/provider'
import App from './App'
import { vi } from 'vitest'

describe('App Component', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('renders', () => {
    render(
      <Provider>
        <App />
      </Provider>
    )

    expect(screen.getByText(/Avaiable Forms/i)).toBeInTheDocument()
  })
})
