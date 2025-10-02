"""
Arama formu render ve validasyon testleri.
Form'un dogru render edildigini ve validasyonlarin calistigini test eder.
"""

from datetime import datetime, timedelta
from src.forms.search_form import SearchForm


class TestSearchFormRender:
    """Arama formu render testleri."""

    def test_index_page_loads(self, client):
        """Ana sayfa basariyla yukleniyor mu?"""
        response = client.get("/")
        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "En Uygun" in html and "Bulun" in html

    def test_form_fields_present(self, client):
        """Form alanlari sayfada mevcut mu?"""
        response = client.get("/")
        assert b"origin" in response.data
        assert b"destination" in response.data
        assert b"departure_date" in response.data
        assert b"return_date" in response.data
        assert b"trip_type" in response.data

    def test_form_labels_accessible(self, client):
        """Form etiketleri erisilebilir mi? (a11y)"""
        response = client.get("/")
        html = response.data.decode("utf-8")
        assert "aria-label" in html
        assert "ehri" in html  # Partial match for Sehri/Şehri
        assert "Varış Şehri" in html


class TestSearchFormValidation:
    """Arama formu validasyon testleri."""

    def test_valid_form_data(self):
        """Gecerli form verisi ile validasyon basarili olmali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        form_data = {
            "origin": "IST",
            "destination": "ESB",
            "departure_date": future_date,
            "trip_type": "one-way",
        }

        form = SearchForm(data=form_data)
        assert form.validate() is True

    def test_missing_origin(self):
        """Kalkis sehri eksikse validasyon basarisiz olmali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        form_data = {
            "destination": "ESB",
            "departure_date": future_date,
            "trip_type": "one-way",
        }

        form = SearchForm(data=form_data)
        assert form.validate() is False
        assert "origin" in form.errors

    def test_invalid_city_code_length(self):
        """Sehir kodu 3 karakterden farkliysa validasyon basarisiz olmali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        form_data = {
            "origin": "ISTANBUL",  # 8 karakter - geçersiz
            "destination": "ESB",
            "departure_date": future_date,
            "trip_type": "one-way",
        }

        form = SearchForm(data=form_data)
        assert form.validate() is False
        assert "origin" in form.errors

    def test_past_departure_date(self):
        """Gecmis tarih girilirse validasyon basarisiz olmali."""
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        form_data = {
            "origin": "IST",
            "destination": "ESB",
            "departure_date": past_date,
            "trip_type": "one-way",
        }

        form = SearchForm(data=form_data)
        assert form.validate() is False
        assert "departure_date" in form.errors

    def test_return_date_before_departure(self):
        """Donus tarihi gidis tarihinden onceyse validasyon basarisiz olmali."""
        departure = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        return_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

        form_data = {
            "origin": "IST",
            "destination": "ESB",
            "departure_date": departure,
            "return_date": return_date,
            "trip_type": "round",
        }

        form = SearchForm(data=form_data)
        assert form.validate() is False
        assert "return_date" in form.errors

    def test_round_trip_missing_return_date(self):
        """Gidis-donus seciliyse ve donus tarihi yoksa validasyon basarisiz olmali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        form_data = {
            "origin": "IST",
            "destination": "ESB",
            "departure_date": future_date,
            "trip_type": "round",
            # return_date yok
        }

        form = SearchForm(data=form_data)
        assert form.validate() is False
        assert "return_date" in form.errors

    def test_city_code_uppercase_conversion(self):
        """Sehir kodlari otomatik olarak buyuk harfe cevrilmeli."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        form_data = {
            "origin": "ist",  # kucuk harf
            "destination": "esb",  # kucuk harf
            "departure_date": future_date,
            "trip_type": "one-way",
        }

        form = SearchForm(data=form_data)
        form.validate()
        assert form.origin.data == "IST"
        assert form.destination.data == "ESB"


class TestSearchFormSubmission:
    """Arama formu gonderim testleri."""

    def test_form_submission_redirects_to_results(self, client):
        """Form gonderildiginde sonuc sayfasina yonlendirme yapilmali."""
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        response = client.post(
            "/flights",
            data={
                "origin": "IST",
                "destination": "ESB",
                "departure_date": future_date,
                "trip_type": "one-way",
            },
            follow_redirects=False,
        )

        assert response.status_code == 200
        html = response.data.decode("utf-8")
        assert "Arama Sonuclari" in html or "bulunan" in html

    def test_invalid_form_shows_errors(self, client):
        """Gecersiz form gonderildiginde hata mesajlari gosterilmeli."""
        response = client.post(
            "/flights",
            data={
                "origin": "",  # bos - gecersiz
                "destination": "ESB",
                "departure_date": "",  # bos - gecersiz
                "trip_type": "one-way",
            },
            follow_redirects=False,
        )

        assert response.status_code == 400
