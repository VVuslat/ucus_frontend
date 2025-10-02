function FlightCard({ flight, onShowDetails }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition duration-200">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        {/* Airline Info */}
        <div className="flex-shrink-0">
          <h3 className="text-lg font-semibold text-gray-800">{flight.airline}</h3>
          <p className="text-sm text-gray-500">{flight.flightNumber}</p>
        </div>

        {/* Flight Times */}
        <div className="flex items-center gap-4 flex-1">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-800">{flight.departure.time}</p>
            <p className="text-sm text-gray-600">{flight.departure.city}</p>
            <p className="text-xs text-gray-500">{flight.departure.airport}</p>
          </div>

          <div className="flex-1 px-4">
            <div className="border-t-2 border-gray-300 relative">
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white px-2">
                <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </div>
            </div>
            <p className="text-xs text-gray-500 text-center mt-2">{flight.duration}</p>
          </div>

          <div className="text-center">
            <p className="text-2xl font-bold text-gray-800">{flight.arrival.time}</p>
            <p className="text-sm text-gray-600">{flight.arrival.city}</p>
            <p className="text-xs text-gray-500">{flight.arrival.airport}</p>
          </div>
        </div>

        {/* Price and Action */}
        <div className="flex-shrink-0 text-center md:text-right">
          <p className="text-3xl font-bold text-blue-600">
            {flight.price}{flight.currency}
          </p>
          <p className="text-sm text-gray-500 mb-3">{flight.class}</p>
          <button
            onClick={() => onShowDetails(flight)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-md transition duration-200"
          >
            Detaylar
          </button>
        </div>
      </div>
    </div>
  );
}

export default FlightCard;
