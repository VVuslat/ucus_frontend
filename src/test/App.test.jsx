import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('renders the main heading', () => {
    render(<App />);
    const heading = screen.getByText(/En uygun fiyatlı uçak biletlerini bulun/i);
    expect(heading).toBeInTheDocument();
  });

  it('renders the search form', () => {
    render(<App />);
    const searchButton = screen.getByRole('button', { name: /Uçuş Ara/i });
    expect(searchButton).toBeInTheDocument();
  });

  it('renders input fields', () => {
    render(<App />);
    expect(screen.getByLabelText(/Nereden/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Nereye/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Tarih/i)).toBeInTheDocument();
  });
});
