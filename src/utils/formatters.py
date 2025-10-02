"""
Tarih, fiyat ve süre formatlama yardımcı fonksiyonları.
Jinja2 template filtreleri olarak kullanılır.
"""

from datetime import datetime
from typing import Union


def format_price(price: Union[float, int], currency: str = "TRY") -> str:
    """
    Fiyatı para birimi ile formatlar.

    Args:
        price: Fiyat değeri
        currency: Para birimi kodu (varsayılan: TRY)

    Returns:
        Formatlanmış fiyat string'i (örn: "1.250,50 TRY")
    """
    try:
        price_float = float(price)
        # Türk para formatı: nokta binlik ayracı, virgül ondalık
        formatted = (
            f"{price_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        return f"{formatted} {currency}"
    except (ValueError, TypeError):
        return f"0,00 {currency}"


def format_datetime(dt_string: str, format_type: str = "full") -> str:
    """
    ISO formatındaki tarih string'ini okunabilir formata çevirir.

    Args:
        dt_string: ISO formatında tarih string'i
        format_type: Format tipi ('full', 'date', 'time')

    Returns:
        Formatlanmış tarih string'i
    """
    try:
        # ISO formatı parse et (timezone bilgisi varsa temizle)
        if "+" in dt_string:
            dt_string = dt_string.split("+")[0]
        elif "Z" in dt_string:
            dt_string = dt_string.replace("Z", "")

        dt = datetime.fromisoformat(dt_string)

        if format_type == "date":
            return dt.strftime("%d.%m.%Y")
        elif format_type == "time":
            return dt.strftime("%H:%M")
        else:  # full
            return dt.strftime("%d.%m.%Y %H:%M")
    except (ValueError, AttributeError):
        return dt_string


def format_duration(minutes: Union[int, float]) -> str:
    """
    Dakika cinsinden süreyi okunabilir formata çevirir.

    Args:
        minutes: Dakika cinsinden süre

    Returns:
        Formatlanmış süre string'i (örn: "2s 30d" veya "1s 15d")
    """
    try:
        total_minutes = int(minutes)
        hours = total_minutes // 60
        mins = total_minutes % 60

        if hours > 0:
            return f"{hours}s {mins}d"
        else:
            return f"{mins}d"
    except (ValueError, TypeError):
        return "0d"


def format_stops(stops: int) -> str:
    """
    Aktarma sayısını Türkçe metin olarak formatlar.

    Args:
        stops: Aktarma sayısı

    Returns:
        Formatlanmış aktarma metni
    """
    if stops == 0:
        return "Direkt"
    elif stops == 1:
        return "1 Aktarma"
    else:
        return f"{stops} Aktarma"
