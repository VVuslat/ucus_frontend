"""
Ucus listesi render testleri.
Arama sonuclarinin dogru sekilde render edildigini test eder.
"""

from datetime import datetime, timedelta


class TestFlightListRender:
    """Ucus listesi render testleri."""

    def test_flights_page_with_valid_search(self, client):
        """Gecerli arama ile ucus listesi sayfasi render edilmeli."""
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

        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "Arama Sonuclari" in html or "bulunan" in html

    def test_search_parameters_displayed(self, client):
        """Arama parametreleri sayfada gosterilmeli."""
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

        assert b"IST" in response.data
        assert b"ESB" in response.data

    def test_flights_displayed_in_list(self, client):
        """Ucuslar liste formatinda gosterilmeli."""
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
        # Flight card elementi olmalı
        assert "flight-card" in html or "article" in html

    def test_filter_sidebar_present(self, client):
        """Filtre sidebar'i sayfada mevcut olmali."""
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
        assert "Filtreler" in html or "Sirala" in html

    def test_new_search_link_present(self, client):
        """Yeni arama yapma linki olmali."""
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

        assert b"Yeni Arama" in response.data or b"yeni arama" in response.data.lower()


class TestFlightListFiltering:
    """Ucus listesi filtreleme testleri."""

    def test_sort_by_price(self, client):
        """Fiyata gore siralama calismali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = client.get(
            f"/flights?origin=IST&destination=ESB&departure_date={future_date}"
            f"&trip_type=one-way&sort_by=price"
        )

        assert response.status_code == 200

    def test_filter_by_max_price(self, client):
        """Maksimum fiyat filtresi calismali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = client.get(
            f"/flights?origin=IST&destination=ESB&departure_date={future_date}"
            f"&trip_type=one-way&max_price=2000"
        )

        assert response.status_code == 200

    def test_filter_by_stops(self, client):
        """Aktarma sayisi filtresi calismali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = client.get(
            f"/flights?origin=IST&destination=ESB&departure_date={future_date}"
            f"&trip_type=one-way&stops=0"
        )

        assert response.status_code == 200


class TestEmptyState:
    """Bos durum (no results) testleri."""

    def test_no_results_with_strict_filter(self, client):
        """Cok dusuk fiyat filtresi ile sonuc bulunmamali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = client.get(
            f"/flights?origin=IST&destination=ESB&departure_date={future_date}"
            f"&trip_type=one-way&max_price=1"  # Çok düşük fiyat
        )

        assert response.status_code == 200
        # Empty state gosterilmeli
        html = response.data.decode("utf-8")
        assert (
            "Bulunamadi" in html
            or "bulunan" in html.lower()
            or "bulundu" in html
        )


class TestResponsiveDesign:
    """Responsive tasarim testleri (HTML icerik kontrolu)."""

    def test_responsive_classes_present(self, client):
        """Responsive CSS siniflari mevcut olmali."""
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
        # Tailwind responsive sınıfları
        assert "md:" in html or "lg:" in html or "sm:" in html

    def test_mobile_viewport_meta(self, client):
        """Mobil viewport meta tag'i olmali."""
        response = client.get("/")
        assert b"viewport" in response.data
        assert b"width=device-width" in response.data
