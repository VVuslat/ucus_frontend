"""
Pytest fixtures ve test konfigürasyonları.
Flask test client ve diğer genel fixture'lar burada tanımlanır.
"""

import pytest
import sys
import os

# Projenin root dizinini Python path'e ekle
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from app import app as flask_app  # noqa: E402
from src.services.flight_service import FlightService  # noqa: E402


@pytest.fixture
def app():
    """Flask uygulaması fixture - test konfigürasyonu ile."""
    flask_app.config.update(
        {
            "TESTING": True,
            # Test sirasinda CSRF kontrolunu devre disi birak
            "WTF_CSRF_ENABLED": False,
        }
    )
    yield flask_app


@pytest.fixture
def client(app):
    """Flask test client fixture."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Flask CLI runner fixture."""
    return app.test_cli_runner()


@pytest.fixture
def flight_service():
    """FlightService instance fixture."""
    return FlightService()


@pytest.fixture
def sample_flight_data():
    """Örnek uçuş verisi fixture - testlerde kullanılmak üzere."""
    return {
        "id": "FLISTESB001",
        "airline": "Turkish Airlines",
        "price": 1250.50,
        "currency": "TRY",
        "departure": "2025-10-10T08:30:00+03:00",
        "arrival": "2025-10-10T10:45:00+03:00",
        "stops": 0,
        "flightNumber": "TK123",
        "aircraft": "A320",
        "policy": "İade edilebilir",
        "origin": "IST",
        "destination": "ESB",
        "duration": 135,
        "baggage": "20kg",
        "cabin_class": "Economy",
        "available_seats": 25,
    }
