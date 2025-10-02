"""
Uçuş servisi - mock API verisi sağlar ve ileride gerçek API entegrasyonu için hazırdır.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random


class FlightService:
    """Uçuş arama ve veri yönetimi servisi."""

    def __init__(self):
        """Servis başlatılır ve örnek havayolu verileri yüklenir."""
        self.airlines = [
            "Turkish Airlines",
            "Pegasus",
            "AnadoluJet",
            "SunExpress",
            "Onur Air",
        ]
        self.aircraft_types = ["A320", "A321", "B737-800", "A330", "B777"]

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        trip_type: str = "one-way",
    ) -> List[Dict]:
        """
        Uçuş arar ve sonuçları döndürür.
        Gerçek uygulamada burada harici API çağrısı yapılır.

        Args:
            origin: Kalkış şehri kodu (örn: IST)
            destination: Varış şehri kodu (örn: ESB)
            departure_date: Gidiş tarihi
            return_date: Dönüş tarihi (opsiyonel)
            trip_type: Yön tipi (one-way veya round)

        Returns:
            Uçuş bilgilerini içeren liste
        """
        return self.get_mock_flights(origin, destination, str(departure_date))

    def get_mock_flights(
        self, origin: str, destination: str, departure_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Mock uçuş verisi üretir - gerçek API taklidi.

        Args:
            origin: Kalkış şehri kodu
            destination: Varış şehri kodu
            departure_date: Gidiş tarihi (string formatında)

        Returns:
            Mock uçuş verisi listesi
        """
        if not departure_date:
            departure_date = datetime.now().date()
        else:
            try:
                departure_date = datetime.fromisoformat(str(departure_date)).date()
            except (ValueError, AttributeError):
                departure_date = datetime.now().date()

        flights = []
        # 5-10 arası rastgele sayıda uçuş üret
        num_flights = random.randint(5, 10)

        for i in range(num_flights):
            flight_id = f"FL{origin}{destination}{i+1:03d}"

            # Rastgele saat üret (06:00 - 22:00 arası)
            departure_hour = random.randint(6, 22)
            departure_minute = random.choice([0, 15, 30, 45])
            departure_dt = datetime.combine(
                departure_date,
                datetime.min.time().replace(
                    hour=departure_hour, minute=departure_minute
                ),
            )

            # Uçuş süresi (1-4 saat arası)
            flight_duration = random.randint(60, 240)
            arrival_dt = departure_dt + timedelta(minutes=flight_duration)

            # Aktarma sayısı (0, 1 veya nadiren 2)
            stops = random.choices([0, 1, 2], weights=[70, 25, 5])[0]

            # Fiyat hesaplama (aktarma sayısına göre)
            base_price = random.uniform(800, 2500)
            price_multiplier = 1 + (stops * 0.15)  # Her aktarma %15 daha pahalı
            final_price = round(base_price * price_multiplier, 2)

            airline = random.choice(self.airlines)
            aircraft = random.choice(self.aircraft_types)

            flight = {
                "id": flight_id,
                "airline": airline,
                "price": final_price,
                "currency": "TRY",
                "departure": departure_dt.isoformat() + "+03:00",
                "arrival": arrival_dt.isoformat() + "+03:00",
                "stops": stops,
                "flightNumber": f"{airline[:2].upper()}{random.randint(100, 999)}",
                "aircraft": aircraft,
                "policy": random.choice(
                    ["İade edilebilir", "İade edilemez", "Değiştirilebilir"]
                ),
                "origin": origin,
                "destination": destination,
                "duration": flight_duration,
                "baggage": random.choice(["20kg", "30kg", "40kg"]),
                "cabin_class": random.choice(["Economy", "Business", "First"]),
                "available_seats": random.randint(5, 50),
            }
            flights.append(flight)

        return flights

    def get_flight_by_id(self, flight_id: str) -> Optional[Dict]:
        """
        ID'ye göre tek bir uçuş bilgisi döndürür.

        Args:
            flight_id: Uçuş ID'si

        Returns:
            Uçuş bilgileri veya None
        """
        # ID'den origin ve destination çıkar
        # Format: FLISTESBxxx gibi
        if not flight_id.startswith("FL") or len(flight_id) < 8:
            return None

        origin = flight_id[2:5]
        destination = flight_id[5:8]

        # Mock veri üret ve ilgili uçuşu bul
        flights = self.get_mock_flights(origin, destination)

        for flight in flights:
            if flight["id"] == flight_id:
                # Ek detaylar ekle
                flight["booking_code"] = f"BK{random.randint(100000, 999999)}"
                flight["meal_service"] = random.choice(
                    ["Kahvaltı", "Öğle yemeği", "Snack", "Yok"]
                )
                flight["entertainment"] = random.choice(
                    ["Film ve müzik", "WiFi", "Yok"]
                )
                return flight

        # Bulunamazsa basit bir mock flight döndür
        return {
            "id": flight_id,
            "airline": random.choice(self.airlines),
            "price": round(random.uniform(1000, 3000), 2),
            "currency": "TRY",
            "departure": datetime.now().isoformat() + "+03:00",
            "arrival": (datetime.now() + timedelta(hours=2)).isoformat() + "+03:00",
            "stops": 0,
            "flightNumber": f"FL{random.randint(100, 999)}",
            "aircraft": random.choice(self.aircraft_types),
            "policy": "İade edilebilir",
            "origin": origin,
            "destination": destination,
            "duration": 120,
            "baggage": "20kg",
            "cabin_class": "Economy",
            "available_seats": 20,
            "booking_code": f"BK{random.randint(100000, 999999)}",
            "meal_service": "Snack",
            "entertainment": "WiFi",
        }
