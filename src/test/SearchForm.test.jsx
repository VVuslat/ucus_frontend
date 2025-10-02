import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import SearchForm from '../components/SearchForm';

describe('SearchForm', () => {
  it('renders all input fields', () => {
    render(<SearchForm onSearch={() => {}} isLoading={false} />);
    
    expect(screen.getByLabelText(/Nereden/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Nereye/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Tarih/i)).toBeInTheDocument();
  });

  it('calls onSearch when form is submitted with valid data', async () => {
    const mockOnSearch = vi.fn();
    render(<SearchForm onSearch={mockOnSearch} isLoading={false} />);

    const fromInput = screen.getByLabelText(/Nereden/i);
    const toInput = screen.getByLabelText(/Nereye/i);
    const dateInput = screen.getByLabelText(/Tarih/i);

    fireEvent.change(fromInput, { target: { value: 'İstanbul' } });
    fireEvent.change(toInput, { target: { value: 'Ankara' } });
    fireEvent.change(dateInput, { target: { value: '2024-03-15' } });

    const form = fromInput.closest('form');
    fireEvent.submit(form);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith({
        from: 'İstanbul',
        to: 'Ankara',
        date: '2024-03-15'
      });
    });
  });

  it('disables button when loading', () => {
    render(<SearchForm onSearch={() => {}} isLoading={true} />);
    
    const submitButton = screen.getByRole('button', { name: /Aranıyor/i });
    expect(submitButton).toBeDisabled();
  });
});
