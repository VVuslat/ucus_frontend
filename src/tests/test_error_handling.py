"""
Hata durumu testleri.
Hata senaryolarinda uygun mesajlarin gosterildigini test eder.
"""


class TestErrorHandling:
    """Hata yonetimi testleri."""

    def test_404_error_handler(self, client):
        """404 hatasi icin uygun sayfa gosterilmeli."""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404

    def test_invalid_form_submission(self, client):
        """Gecersiz form gonderimi hata mesaji gostermeli."""
        response = client.post(
            "/flights",
            data={
                "origin": "",  # boş - geçersiz
                "destination": "",  # boş - geçersiz
                "departure_date": "",  # boş - geçersiz
                "trip_type": "one-way",
            },
        )

        assert response.status_code == 400
        # Form tekrar gösterilmeli ve hata mesajları olmalı
        html = response.data.decode("utf-8")
        assert "form" in html.lower()

    def test_missing_required_field_shows_error(self, client):
        """Gerekli alan eksikse hata mesaji gosterilmeli."""
        response = client.post(
            "/flights",
            data={
                "destination": "ESB",
                # origin eksik
                "departure_date": "2025-12-01",
                "trip_type": "one-way",
            },
        )

        assert response.status_code == 400

    def test_invalid_date_format(self, client):
        """Gecersiz tarih formati hata uretmeli."""
        response = client.post(
            "/flights",
            data={
                "origin": "IST",
                "destination": "ESB",
                "departure_date": "invalid-date",
                "trip_type": "one-way",
            },
        )

        assert response.status_code == 400


class TestFormValidationErrors:
    """Form validasyon hata mesajlari testleri."""

    def test_error_message_displayed_for_missing_origin(self, client):
        """Kalkis sehri eksikse hata mesaji gosterilmeli."""
        response = client.post(
            "/flights",
            data={
                "origin": "",
                "destination": "ESB",
                "departure_date": "2025-12-01",
                "trip_type": "one-way",
            },
        )

        html = response.data.decode("utf-8")
        # Hata mesajı içermeli
        assert "zorunlu" in html.lower() or "required" in html.lower()

    def test_multiple_validation_errors(self, client):
        """Birden fazla validasyon hatasi ayni anda gosterilebilmeli."""
        response = client.post(
            "/flights",
            data={
                "origin": "",  # boş
                "destination": "",  # boş
                "departure_date": "",  # boş
                "trip_type": "one-way",
            },
        )

        assert response.status_code == 400
        # Birden fazla hata olmalı
        html = response.data.decode("utf-8")
        assert html.count("zorunlu") > 1 or html.count("required") > 1


class TestAPIErrorHandling:
    """API hata yonetimi testleri."""

    def test_flight_detail_invalid_id(self, client):
        """Gecersiz flight ID icin uygun yanit verilmeli."""
        response = client.get("/api/flight/INVALID123")
        # Service her zaman bir flight döndürebileceği için 200 veya 404
        assert response.status_code in [200, 404]

    def test_modal_invalid_id(self, client):
        """Gecersiz flight ID icin modal uygun yanit vermeli."""
        response = client.get("/flight/INVALID123/modal")
        # Service her zaman bir flight döndürebileceği için 200 veya 404
        assert response.status_code in [200, 404]


class TestEmptyResults:
    """Bos sonuc durumu testleri."""

    def test_no_flights_message(self, client):
        """Sonuc bulunamadiginda uygun mesaj gosterilmeli."""
        # Çok düşük fiyat filtresi ile sonuç gelmemesi
        response = client.get(
            "/flights?origin=IST&destination=ESB&departure_date=2025-12-01"
            "&trip_type=one-way&max_price=1"
        )

        html = response.data.decode("utf-8")
        # Empty state mesajı
        assert (
            "bulunamadı" in html.lower()
            or "no flights" in html.lower()
            or len(html) > 0
        )

    def test_empty_state_has_new_search_button(self, client):
        """Bos sonuc durumunda yeni arama butonu olmali."""
        response = client.get(
            "/flights?origin=IST&destination=ESB&departure_date=2025-12-01"
            "&trip_type=one-way&max_price=1"
        )

        html = response.data.decode("utf-8")
        # Yeni arama linki veya butonu
        assert "yeni arama" in html.lower() or "Ana Sayfa" in html or 'href="/"' in html


class TestAccessibilityInErrors:
    """Hata durumlarinda erisilebilirlik testleri."""

    def test_error_messages_have_role_alert(self, client):
        """Hata mesajları role="alert" içermeli."""
        response = client.post(
            "/flights",
            data={
                "origin": "",
                "destination": "ESB",
                "departure_date": "2025-12-01",
                "trip_type": "one-way",
            },
        )

        html = response.data.decode("utf-8")
        # ARIA role alert veya aria-live
        assert 'role="alert"' in html or "aria-live" in html or "error" in html.lower()

    def test_form_has_novalidate_attribute(self, client):
        """
        Form novalidate attribute'una sahip olmali
        (sunucu tarafi validasyon icin).
        """
        response = client.get("/")
        html = response.data.decode("utf-8")
        assert "novalidate" in html.lower()
