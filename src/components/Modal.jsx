import { useEffect } from 'react';

function Modal({ isOpen, onClose, flight, details }) {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen || !flight) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
        ></div>

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          {/* Header */}
          <div className="bg-blue-600 px-6 py-4 flex justify-between items-center">
            <h3 className="text-xl font-bold text-white">Uçuş Detayları</h3>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-4">
            {/* Airline and Flight Number */}
            <div className="mb-6">
              <h4 className="text-2xl font-bold text-gray-800">{flight.airline}</h4>
              <p className="text-gray-600">Uçuş No: {flight.flightNumber}</p>
            </div>

            {/* Flight Route */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="text-center">
                <p className="text-sm text-gray-500 mb-1">Kalkış</p>
                <p className="text-3xl font-bold text-gray-800">{flight.departure.time}</p>
                <p className="text-lg text-gray-700">{flight.departure.city}</p>
                <p className="text-sm text-gray-500">{flight.departure.airport}</p>
                <p className="text-sm text-gray-500">{flight.departure.date}</p>
              </div>

              <div className="flex flex-col items-center justify-center">
                <svg className="w-8 h-8 text-blue-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
                <p className="text-sm text-gray-600">{flight.duration}</p>
              </div>

              <div className="text-center">
                <p className="text-sm text-gray-500 mb-1">Varış</p>
                <p className="text-3xl font-bold text-gray-800">{flight.arrival.time}</p>
                <p className="text-lg text-gray-700">{flight.arrival.city}</p>
                <p className="text-sm text-gray-500">{flight.arrival.airport}</p>
                <p className="text-sm text-gray-500">{flight.arrival.date}</p>
              </div>
            </div>

            {/* Additional Details */}
            {details && (
              <div className="border-t pt-4 space-y-4">
                <div>
                  <p className="text-sm font-semibold text-gray-700">Sınıf</p>
                  <p className="text-gray-600">{flight.class}</p>
                </div>
                
                <div>
                  <p className="text-sm font-semibold text-gray-700">Bagaj Hakkı</p>
                  <p className="text-gray-600">{details.baggage}</p>
                </div>

                <div>
                  <p className="text-sm font-semibold text-gray-700">İptal Politikası</p>
                  <p className="text-gray-600">{details.cancellationPolicy}</p>
                </div>

                <div>
                  <p className="text-sm font-semibold text-gray-700">İkramlar</p>
                  <ul className="list-disc list-inside text-gray-600">
                    {details.amenities.map((amenity, index) => (
                      <li key={index}>{amenity}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Price */}
            <div className="mt-6 pt-4 border-t flex justify-between items-center">
              <span className="text-gray-700 font-semibold">Toplam Fiyat:</span>
              <span className="text-3xl font-bold text-blue-600">
                {flight.price}{flight.currency}
              </span>
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-4 flex justify-end gap-3">
            <button
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100 transition"
            >
              Kapat
            </button>
            <button
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
            >
              Satın Al
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Modal;
