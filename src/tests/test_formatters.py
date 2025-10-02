"""
Utility formatters testleri.
Tarih, fiyat ve sure formatlama fonksiyonlarini test eder.
"""

from src.utils.formatters import (
    format_price,
    format_datetime,
    format_duration,
    format_stops,
)


class TestPriceFormatter:
    """Fiyat formatlama testleri."""

    def test_format_price_basic(self):
        """Basit fiyat formatlamasi calismali."""
        result = format_price(1250.50, "TRY")
        assert "1.250,50" in result
        assert "TRY" in result

    def test_format_price_integer(self):
        """Integer fiyat formatlamasi calismali."""
        result = format_price(1000, "TRY")
        assert "1.000,00" in result
        assert "TRY" in result

    def test_format_price_large_number(self):
        """Buyuk sayilar icin formatlamasi calismali."""
        result = format_price(123456.78, "TRY")
        assert "123.456,78" in result

    def test_format_price_default_currency(self):
        """Varsayilan para birimi TRY olmali."""
        result = format_price(1000)
        assert "TRY" in result

    def test_format_price_invalid_input(self):
        """Gecersiz input icin varsayilan deger donmeli."""
        result = format_price("invalid", "TRY")
        assert "0,00 TRY" in result


class TestDateTimeFormatter:
    """Tarih-saat formatlama testleri."""

    def test_format_datetime_full(self):
        """Tam tarih-saat formatlamasi calismali."""
        dt_string = "2025-10-10T08:30:00+03:00"
        result = format_datetime(dt_string, "full")
        assert "10.10.2025" in result
        assert "08:30" in result

    def test_format_datetime_date_only(self):
        """Sadece tarih formatlamasi calismali."""
        dt_string = "2025-10-10T08:30:00+03:00"
        result = format_datetime(dt_string, "date")
        assert "10.10.2025" in result
        assert "08:30" not in result

    def test_format_datetime_time_only(self):
        """Sadece saat formatlamasi calismali."""
        dt_string = "2025-10-10T08:30:00+03:00"
        result = format_datetime(dt_string, "time")
        assert "08:30" in result
        assert "2025" not in result

    def test_format_datetime_with_z_timezone(self):
        """Z timezone ile formatlamasi calismali."""
        dt_string = "2025-10-10T08:30:00Z"
        result = format_datetime(dt_string, "time")
        assert "08:30" in result

    def test_format_datetime_invalid_input(self):
        """Gecersiz input icin orijinal string donmeli."""
        dt_string = "invalid-date"
        result = format_datetime(dt_string)
        assert result == dt_string


class TestDurationFormatter:
    """Sure formatlama testleri."""

    def test_format_duration_hours_and_minutes(self):
        """Saat ve dakika formatlamasi calismali."""
        result = format_duration(150)  # 2 saat 30 dakika
        assert "2s" in result
        assert "30d" in result

    def test_format_duration_only_minutes(self):
        """Sadece dakika formatlamasi calismali."""
        result = format_duration(45)
        assert "45d" in result
        assert "s" not in result or "0s" in result

    def test_format_duration_exact_hours(self):
        """Tam saat formatlamasi calismali."""
        result = format_duration(120)  # 2 saat
        assert "2s" in result
        assert "0d" in result

    def test_format_duration_float_input(self):
        """Float input calismali."""
        result = format_duration(90.5)
        assert "1s" in result
        assert "30d" in result

    def test_format_duration_invalid_input(self):
        """Gecersiz input icin varsayilan deger donmeli."""
        result = format_duration("invalid")
        assert "0d" in result


class TestStopsFormatter:
    """Aktarma sayisi formatlama testleri."""

    def test_format_stops_zero(self):
        """Sifir aktarma icin 'Direkt' donmeli."""
        result = format_stops(0)
        assert result == "Direkt"

    def test_format_stops_one(self):
        """Bir aktarma icin '1 Aktarma' donmeli."""
        result = format_stops(1)
        assert result == "1 Aktarma"

    def test_format_stops_multiple(self):
        """Birden fazla aktarma icin sayi + 'Aktarma' donmeli."""
        result = format_stops(2)
        assert result == "2 Aktarma"

    def test_format_stops_large_number(self):
        """Buyuk sayilar icin formatlamasi calismali."""
        result = format_stops(5)
        assert result == "5 Aktarma"


class TestFormattersIntegration:
    """Formatlayicilarin birlikte kullanimi testleri."""

    def test_formatters_with_sample_flight(self, sample_flight_data):
        """Ornek ucus verisi ile formatlayicilar calismali."""
        price = format_price(
            sample_flight_data["price"], sample_flight_data["currency"]
        )
        assert "TRY" in price

        departure = format_datetime(sample_flight_data["departure"], "time")
        assert ":" in departure  # Saat formatı

        duration = format_duration(sample_flight_data["duration"])
        assert "s" in duration or "d" in duration

        stops = format_stops(sample_flight_data["stops"])
        assert stops == "Direkt"
