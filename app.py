"""
Flask uygulaması - MYK Yazılım Geliştirici Seviye 5 uyumlu uçak bileti arama frontend.
Mock API, Jinja2 şablonları ve responsive tasarım içerir.
"""

from flask import Flask, render_template, request, jsonify
from src.forms.search_form import SearchForm
from src.services.flight_service import FlightService
from src.utils.formatters import format_price, format_datetime, format_duration

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.config["SECRET_KEY"] = "myk-ucus-frontend-secret-key-2025"
app.config["WTF_CSRF_ENABLED"] = True

flight_service = FlightService()


@app.route("/")
def index():
    """Ana sayfa - arama formu."""
    form = SearchForm()
    return render_template("index.html", form=form)


@app.route("/flights", methods=["GET", "POST"])
def flights():
    """
    Uçuş arama sonuçları sayfası.
    Form verilerini alır, mock API'den sonuçları çeker ve şablona gönderir.
    """
    form = SearchForm(request.form if request.method == "POST" else request.args)

    if form.validate():
        # Form verilerini al
        origin = form.origin.data
        destination = form.destination.data
        departure_date = form.departure_date.data
        return_date = form.return_date.data if form.trip_type.data == "round" else None
        trip_type = form.trip_type.data

        # Query parametrelerinden filtre ve sıralama al
        sort_by = request.args.get("sort_by", "price")
        filter_max_price = request.args.get("max_price", type=float)
        filter_stops = request.args.get("stops", type=int)

        # Mock API'den uçuş verilerini al
        flights_data = flight_service.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            trip_type=trip_type,
        )

        # Filtreleme uygula
        if filter_max_price:
            flights_data = [f for f in flights_data if f["price"] <= filter_max_price]
        if filter_stops is not None:
            flights_data = [f for f in flights_data if f["stops"] == filter_stops]

        # Sıralama uygula
        if sort_by == "price":
            flights_data.sort(key=lambda x: x["price"])
        elif sort_by == "departure":
            flights_data.sort(key=lambda x: x["departure"])

        return render_template(
            "flights_list.html",
            flights=flights_data,
            form=form,
            search_params={
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "trip_type": trip_type,
            },
            sort_by=sort_by,
            filter_max_price=filter_max_price,
            filter_stops=filter_stops,
        )
    else:
        # Form geçersizse hata mesajlarıyla birlikte arama sayfasını göster
        return render_template("index.html", form=form), 400


@app.route("/api/mock/flights")
def mock_flights_api():
    """
    Mock API endpoint - gerçek bir harici API taklidi.
    Query parametrelerine göre örnek uçuş verisi döndürür.
    """
    origin = request.args.get("origin", "IST")
    destination = request.args.get("destination", "ESB")
    departure_date = request.args.get("departure_date")

    flights_data = flight_service.get_mock_flights(
        origin=origin, destination=destination, departure_date=departure_date
    )

    return jsonify({"flights": flights_data, "total": len(flights_data)})


@app.route("/api/flight/<flight_id>")
def flight_detail_api(flight_id):
    """
    Tek bir uçuşun detaylı bilgilerini döndüren API endpoint.
    Modal içeriği için kullanılır.
    """
    flight = flight_service.get_flight_by_id(flight_id)
    if flight:
        return jsonify(flight)
    else:
        return jsonify({"error": "Uçuş bulunamadı"}), 404


@app.route("/flight/<flight_id>/modal")
def flight_modal(flight_id):
    """
    Uçuş detay modal'ının HTML içeriğini döndürür.
    AJAX ile yüklenmek üzere tasarlanmıştır.
    """
    flight = flight_service.get_flight_by_id(flight_id)
    if flight:
        return render_template("flight_detail_modal.html", flight=flight)
    else:
        return "<p>Uçuş bulunamadı.</p>", 404


# Template filtrelerini ekle
app.jinja_env.filters["format_price"] = format_price
app.jinja_env.filters["format_datetime"] = format_datetime
app.jinja_env.filters["format_duration"] = format_duration


@app.errorhandler(404)
def not_found(error):
    """404 hatası için özel sayfa."""
    from src.forms.search_form import SearchForm

    form = SearchForm()
    return render_template("index.html", error="Sayfa bulunamadı", form=form), 404


@app.errorhandler(500)
def server_error(error):
    """500 hatası için özel sayfa."""
    from src.forms.search_form import SearchForm

    form = SearchForm()
    return render_template("index.html", error="Sunucu hatası oluştu", form=form), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
