"""Form validasyonu için WTForms kullanılarak oluşturulmuş arama formu."""

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime


class SearchForm(FlaskForm):
    """Uçuş arama formu - kalkış, varış, tarih ve yön seçimi."""

    origin = StringField(
        "Kalkış Şehri",
        validators=[
            DataRequired(message="Kalkış şehri zorunludur"),
            Length(min=3, max=3, message="Şehir kodu 3 karakter olmalıdır (örn: IST)"),
        ],
        render_kw={
            "placeholder": "IST",
            "class": "form-input",
            "aria-label": "Kalkış şehri kodu",
        },
    )

    destination = StringField(
        "Varış Şehri",
        validators=[
            DataRequired(message="Varış şehri zorunludur"),
            Length(min=3, max=3, message="Şehir kodu 3 karakter olmalıdır (örn: ESB)"),
        ],
        render_kw={
            "placeholder": "ESB",
            "class": "form-input",
            "aria-label": "Varış şehri kodu",
        },
    )

    departure_date = DateField(
        "Gidiş Tarihi",
        validators=[DataRequired(message="Gidiş tarihi zorunludur")],
        format="%Y-%m-%d",
        render_kw={"class": "form-input", "aria-label": "Gidiş tarihi"},
    )

    return_date = DateField(
        "Dönüş Tarihi",
        format="%Y-%m-%d",
        render_kw={"class": "form-input", "aria-label": "Dönüş tarihi"},
    )

    trip_type = SelectField(
        "Yön",
        choices=[("one-way", "Tek Yön"), ("round", "Gidiş-Dönüş")],
        default="one-way",
        validators=[DataRequired()],
        render_kw={"class": "form-select", "aria-label": "Yön seçimi"},
    )

    def validate_origin(self, field):
        """Kalkış şehri kodunu büyük harfe çevir ve geçerliliğini kontrol et."""
        if field.data:
            field.data = field.data.upper()
            # Gerçek uygulamada geçerli havalimanı kodları kontrol edilir
            if not field.data.isalpha():
                raise ValidationError("Şehir kodu yalnızca harf içermelidir")

    def validate_destination(self, field):
        """Varış şehri kodunu büyük harfe çevir ve geçerliliğini kontrol et."""
        if field.data:
            field.data = field.data.upper()
            if not field.data.isalpha():
                raise ValidationError("Şehir kodu yalnızca harf içermelidir")

    def validate_departure_date(self, field):
        """Gidiş tarihinin bugün veya gelecek bir tarih olduğunu kontrol et."""
        if field.data and field.data < datetime.now().date():
            raise ValidationError("Gidiş tarihi bugün veya gelecek bir tarih olmalıdır")

    def validate_return_date(self, field):
        """
        Dönüş tarihinin gidiş tarihinden sonra olduğunu kontrol et.
        Sadece gidiş-dönüş seçiliyse geçerlidir.
        """
        if self.trip_type.data == "round" and field.data:
            if field.data < self.departure_date.data:
                raise ValidationError(
                    "Dönüş tarihi gidiş tarihinden önce olamaz"
                )
        elif self.trip_type.data == "round" and not field.data:
            raise ValidationError(
                "Gidiş-dönüş için dönüş tarihi zorunludur"
            )
