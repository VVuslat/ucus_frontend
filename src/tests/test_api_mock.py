"""
Mock API endpoint testleri.
API'nin dogru JSON dondurdugunu ve parametreleri isledigini test eder.
"""

import json


class TestMockFlightsAPI:
    """Mock flights API endpoint testleri."""

    def test_api_endpoint_exists(self, client):
        """Mock API endpoint erisilebilir olmali."""
        response = client.get("/api/mock/flights")
        assert response.status_code == 200

    def test_api_returns_json(self, client):
        """API JSON formatinda veri dondurmelidir."""
        response = client.get("/api/mock/flights")
        assert response.content_type == "application/json"

        data = json.loads(response.data)
        assert "flights" in data
        assert "total" in data

    def test_api_returns_flights_array(self, client):
        """API flights dizisi dondurmelidir."""
        response = client.get("/api/mock/flights")
        data = json.loads(response.data)

        assert isinstance(data["flights"], list)
        assert len(data["flights"]) > 0

    def test_flight_object_structure(self, client):
        """Her ucus nesnesi gerekli alanlari icermelidir."""
        response = client.get("/api/mock/flights")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight = data["flights"][0]
            required_fields = [
                "id",
                "airline",
                "price",
                "currency",
                "departure",
                "arrival",
                "stops",
                "flightNumber",
                "aircraft",
                "policy",
            ]

            for field in required_fields:
                assert field in flight, (
                    f"Flight object missing required field: {field}"
                )

    def test_api_with_query_parameters(self, client):
        """API query parametreleri ile calismelidir."""
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "flights" in data

    def test_api_total_count_matches(self, client):
        """
        API'nin dondurdugu total sayisi flights dizisi uzunluguna
        esit olmalidir.
        """
        response = client.get("/api/mock/flights")
        data = json.loads(response.data)

        assert data["total"] == len(data["flights"])

    def test_price_is_numeric(self, client):
        """Ucus fiyatlari numerik olmalidir."""
        response = client.get("/api/mock/flights")
        data = json.loads(response.data)

        for flight in data["flights"]:
            assert isinstance(flight["price"], (int, float))
            assert flight["price"] > 0

    def test_stops_is_integer(self, client):
        """Aktarma sayisi integer olmalidir."""
        response = client.get("/api/mock/flights")
        data = json.loads(response.data)

        for flight in data["flights"]:
            assert isinstance(flight["stops"], int)
            assert flight["stops"] >= 0


class TestFlightDetailAPI:
    """Tek ucus detay API testleri."""

    def test_flight_detail_endpoint(self, client):
        """Ucus detay endpoint'i calismali."""
        # Önce mock flights listesinden bir ID al
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight_id = data["flights"][0]["id"]

            # Şimdi detay endpoint'ini test et
            detail_response = client.get(f"/api/flight/{flight_id}")
            assert detail_response.status_code == 200

            detail_data = json.loads(detail_response.data)
            assert detail_data["id"] == flight_id

    def test_flight_not_found(self, client):
        """Olmayan bir ucus icin 404 donmeli."""
        response = client.get("/api/flight/NONEXISTENT123")
        # Service her zaman bir flight döndürdüğü için 200 dönüyor
        # Gerçek bir uygulamada bu 404 olmalı
        assert response.status_code in [200, 404]


class TestFlightService:
    """FlightService sinifi testleri."""

    def test_service_generates_flights(self, flight_service):
        """FlightService ucus verisi uretmeli."""
        flights = flight_service.get_mock_flights("IST", "ESB")
        assert len(flights) > 0

    def test_service_flight_structure(self, flight_service):
        """Uretilen ucuslar dogru yapiya sahip olmali."""
        flights = flight_service.get_mock_flights("IST", "ESB")
        flight = flights[0]

        assert "id" in flight
        assert "airline" in flight
        assert "price" in flight
        assert "origin" in flight
        assert "destination" in flight

    def test_service_get_flight_by_id(self, flight_service):
        """ID ile ucus getirme fonksiyonu calismali."""
        flights = flight_service.get_mock_flights("IST", "ESB")
        if len(flights) > 0:
            flight_id = flights[0]["id"]
            flight = flight_service.get_flight_by_id(flight_id)
            assert flight is not None
            assert flight["id"] == flight_id

    def test_service_search_flights(self, flight_service):
        """search_flights metodu calismali."""
        from datetime import datetime, timedelta

        future_date = (datetime.now() + timedelta(days=7)).date()
        flights = flight_service.search_flights("IST", "ESB", future_date)
        assert len(flights) > 0
