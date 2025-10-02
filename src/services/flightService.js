// Mock flight data
const mockFlights = [
  {
    id: 1,
    airline: 'Turkish Airlines',
    flightNumber: 'TK1234',
    departure: {
      city: 'İstanbul',
      airport: 'IST',
      time: '10:00',
      date: '2024-03-15'
    },
    arrival: {
      city: 'Ankara',
      airport: 'ESB',
      time: '11:15',
      date: '2024-03-15'
    },
    price: 450,
    currency: '₺',
    duration: '1s 15dk',
    class: 'Ekonomi'
  },
  {
    id: 2,
    airline: 'Pegasus Airlines',
    flightNumber: 'PC5678',
    departure: {
      city: 'İstanbul',
      airport: 'SAW',
      time: '14:30',
      date: '2024-03-15'
    },
    arrival: {
      city: 'Ankara',
      airport: 'ESB',
      time: '15:45',
      date: '2024-03-15'
    },
    price: 380,
    currency: '₺',
    duration: '1s 15dk',
    class: 'Ekonomi'
  },
  {
    id: 3,
    airline: 'AnadoluJet',
    flightNumber: 'TK7890',
    departure: {
      city: 'İstanbul',
      airport: 'IST',
      time: '18:00',
      date: '2024-03-15'
    },
    arrival: {
      city: 'Ankara',
      airport: 'ESB',
      time: '19:15',
      date: '2024-03-15'
    },
    price: 420,
    currency: '₺',
    duration: '1s 15dk',
    class: 'Ekonomi'
  }
];

// Simulate API delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Search flights API
export const searchFlights = async (searchParams) => {
  await delay(800); // Simulate network delay
  
  const { from, to, date } = searchParams;
  
  if (!from || !to || !date) {
    throw new Error('Eksik parametre');
  }
  
  // Filter and customize mock data based on search params
  const results = mockFlights.map(flight => ({
    ...flight,
    departure: {
      ...flight.departure,
      city: from,
      date: date
    },
    arrival: {
      ...flight.arrival,
      city: to,
      date: date
    }
  }));
  
  return results;
};

// Get flight details by ID
export const getFlightDetails = async (flightId) => {
  await delay(500);
  
  const flight = mockFlights.find(f => f.id === flightId);
  
  if (!flight) {
    throw new Error('Uçuş bulunamadı');
  }
  
  return {
    ...flight,
    baggage: '15kg',
    cancellationPolicy: 'Ücretsiz iptal: 24 saat öncesine kadar',
    amenities: ['Ücretsiz içecek', 'USB şarj', 'WiFi']
  };
};
