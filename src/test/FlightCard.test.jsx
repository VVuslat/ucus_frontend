import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import FlightCard from '../components/FlightCard';

describe('FlightCard', () => {
  const mockFlight = {
    id: 1,
    airline: 'Turkish Airlines',
    flightNumber: 'TK1234',
    departure: {
      city: 'İstanbul',
      airport: 'IST',
      time: '10:00'
    },
    arrival: {
      city: 'Ankara',
      airport: 'ESB',
      time: '11:15'
    },
    price: 450,
    currency: '₺',
    duration: '1s 15dk',
    class: 'Ekonomi'
  };

  it('renders flight information', () => {
    render(<FlightCard flight={mockFlight} onShowDetails={() => {}} />);
    
    expect(screen.getByText('Turkish Airlines')).toBeInTheDocument();
    expect(screen.getByText('TK1234')).toBeInTheDocument();
    expect(screen.getByText('10:00')).toBeInTheDocument();
    expect(screen.getByText('11:15')).toBeInTheDocument();
    expect(screen.getByText('İstanbul')).toBeInTheDocument();
    expect(screen.getByText('Ankara')).toBeInTheDocument();
  });

  it('displays price correctly', () => {
    render(<FlightCard flight={mockFlight} onShowDetails={() => {}} />);
    
    expect(screen.getByText(/450₺/)).toBeInTheDocument();
  });

  it('calls onShowDetails when details button is clicked', () => {
    const mockOnShowDetails = vi.fn();
    render(<FlightCard flight={mockFlight} onShowDetails={mockOnShowDetails} />);
    
    const detailsButton = screen.getByText('Detaylar');
    detailsButton.click();
    
    expect(mockOnShowDetails).toHaveBeenCalledWith(mockFlight);
  });
});
