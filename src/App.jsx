import { useState } from 'react';
import SearchForm from './components/SearchForm';
import FlightList from './components/FlightList';
import Modal from './components/Modal';
import { searchFlights, getFlightDetails } from './services/flightService';

function App() {
  const [flights, setFlights] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [flightDetails, setFlightDetails] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSearch = async (searchParams) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const results = await searchFlights(searchParams);
      setFlights(results);
    } catch (err) {
      setError(err.message);
      setFlights([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleShowDetails = async (flight) => {
    setSelectedFlight(flight);
    setIsModalOpen(true);
    
    try {
      const details = await getFlightDetails(flight.id);
      setFlightDetails(details);
    } catch (err) {
      console.error('Detaylar yüklenemedi:', err);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedFlight(null);
    setFlightDetails(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-2">
            ✈️ Uçuş Arama
          </h1>
          <p className="text-gray-600">
            En uygun fiyatlı uçak biletlerini bulun
          </p>
        </div>

        {/* Search Form */}
        <SearchForm onSearch={handleSearch} isLoading={isLoading} />

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Uçuşlar aranıyor...</p>
          </div>
        )}

        {/* Flight List */}
        {!isLoading && flights.length > 0 && (
          <FlightList flights={flights} onShowDetails={handleShowDetails} />
        )}

        {/* Modal */}
        <Modal
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          flight={selectedFlight}
          details={flightDetails}
        />
      </div>
    </div>
  );
}

export default App;

