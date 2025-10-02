import FlightCard from './FlightCard';

function FlightList({ flights, onShowDetails }) {
  if (!flights || flights.length === 0) {
    return (
      <div className="text-center py-12">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <h3 className="mt-2 text-lg font-medium text-gray-900">Uçuş bulunamadı</h3>
        <p className="mt-1 text-sm text-gray-500">
          Lütfen farklı arama kriterleri ile tekrar deneyin.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        {flights.length} Uçuş Bulundu
      </h2>
      {flights.map(flight => (
        <FlightCard 
          key={flight.id} 
          flight={flight} 
          onShowDetails={onShowDetails}
        />
      ))}
    </div>
  );
}

export default FlightList;
