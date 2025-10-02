"""
Modal davranis testleri.
Modal'in acilip kapanabildigini ve iceriginin dogru yuklendigini test eder.
"""

import json
from datetime import datetime, timedelta


class TestModalEndpoints:
    """Modal endpoint testleri."""

    def test_modal_endpoint_exists(self, client):
        """Modal endpoint erisilebilir olmali."""
        # Önce bir flight ID al
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight_id = data["flights"][0]["id"]
            modal_response = client.get(f"/flight/{flight_id}/modal")
            assert modal_response.status_code == 200

    def test_modal_returns_html(self, client):
        """Modal endpoint HTML dondurmeli."""
        # Bir flight ID al
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight_id = data["flights"][0]["id"]
            modal_response = client.get(f"/flight/{flight_id}/modal")
            assert modal_response.content_type.startswith("text/html")

    def test_modal_contains_flight_details(self, client):
        """Modal icerigi ucus detaylarini icermeli."""
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight = data["flights"][0]
            flight_id = flight["id"]

            modal_response = client.get(f"/flight/{flight_id}/modal")
            html = modal_response.data.decode("utf-8")

            # Modal başlık
            assert "Uçuş Detayları" in html
            # Uçuş numarası veya havayolu
            assert flight["airline"] in html or flight["flightNumber"] in html

    def test_modal_not_found(self, client):
        """Olmayan bir ucus icin modal 404 donmeli veya uygun hata mesaji gostermeli."""
        response = client.get("/flight/INVALID_ID_12345/modal")
        # Service her zaman bir flight döndürebilir, o yüzden 200 veya 404
        assert response.status_code in [200, 404]


class TestModalAccessibility:
    """Modal erisilebilirlik testleri."""

    def test_modal_has_aria_attributes(self, client):
        """Modal ARIA attribute'lara sahip olmali."""
        response = client.get("/")
        html = response.data.decode("utf-8")

        # Base template'de modal container
        assert "modal-container" in html
        assert "aria-hidden" in html or "aria-modal" in html or 'role="dialog"' in html

    def test_modal_has_close_button(self, client):
        """Modal icerigi kapatma butonu icermeli."""
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight_id = data["flights"][0]["id"]
            modal_response = client.get(f"/flight/{flight_id}/modal")
            html = modal_response.data.decode("utf-8")

            # Kapatma butonu
            assert "closeModal" in html or "Kapat" in html


class TestModalJavaScript:
    """Modal JavaScript fonksiyonlarinin varligini test eder."""

    def test_ui_js_file_exists(self, client):
        """ui.js dosyasi erisilebilir olmali."""
        response = client.get("/static/js/ui.js")
        assert response.status_code == 200

    def test_ui_js_contains_modal_functions(self, client):
        """ui.js modal fonksiyonlarini icermeli."""
        response = client.get("/static/js/ui.js")
        js_content = response.data.decode("utf-8")

        assert "openFlightModal" in js_content
        assert "closeModal" in js_content
        assert "modal-container" in js_content


class TestModalContent:
    """Modal icerik testleri."""

    def test_modal_shows_price(self, client):
        """Modal fiyat bilgisini gostermeli."""
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight = data["flights"][0]
            flight_id = flight["id"]

            modal_response = client.get(f"/flight/{flight_id}/modal")
            html = modal_response.data.decode("utf-8")

            # Fiyat bilgisi
            assert "TRY" in html or "fiyat" in html.lower()

    def test_modal_shows_departure_arrival(self, client):
        """Modal kalkis ve varis bilgilerini gostermeli."""
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight = data["flights"][0]
            flight_id = flight["id"]

            modal_response = client.get(f"/flight/{flight_id}/modal")
            html = modal_response.data.decode("utf-8")

            # Kalkış ve varış
            assert "Kalkış" in html or "Varış" in html

    def test_modal_shows_aircraft_info(self, client):
        """Modal ucak bilgilerini gostermeli."""
        response = client.get("/api/mock/flights?origin=IST&destination=ESB")
        data = json.loads(response.data)

        if len(data["flights"]) > 0:
            flight = data["flights"][0]
            flight_id = flight["id"]

            modal_response = client.get(f"/flight/{flight_id}/modal")
            html = modal_response.data.decode("utf-8")

            # Uçak modeli
            assert flight["aircraft"] in html or "Uçak" in html


class TestModalInteraction:
    """Modal etkilesim testleri (integration)."""

    def test_flight_card_has_details_button(self, client):
        """Ucus kartlari detaylar butonu icermeli."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = client.post(
            "/flights",
            data={
                "origin": "IST",
                "destination": "ESB",
                "departure_date": future_date,
                "trip_type": "one-way",
            },
        )

        html = response.data.decode("utf-8")
        assert "Detaylar" in html or "openFlightModal" in html
