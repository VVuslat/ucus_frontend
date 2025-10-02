# Uçuş Frontend - MYK Uyumlu Uçak Bileti Arama Platformu

Flask + Jinja2 ile hazırlanmış, MYK Yazılım Geliştirici Seviye 5 yönergesine uygun uçak bileti arama & takip frontend projesi. Mock API, responsive tasarım ve pytest tabanlı testlerle teslim edilir.

## 📋 Proje Açıklaması

Bu uygulama sayesinde gitmek istediğiniz bölgeyi girdiğinizde bu bölgeye giden en uygun fiyatlı uçak biletini görüntüleyebilirsiniz. Proje, MYK (Mesleki Yeterlilik Kurumu) Yazılım Geliştirici Seviye 5 yönergesine tam uyumlu olarak geliştirilmiştir.

### ✨ Özellikler

- 🔍 **Hızlı Arama**: Kalkış, varış, tarih ve yön seçimi ile uçuş arama
- 💰 **Fiyat Karşılaştırma**: Farklı havayollarının fiyatlarını karşılaştırma
- 🔄 **Filtreleme ve Sıralama**: Fiyat, kalkış saati ve aktarma sayısına göre filtreleme
- 📱 **Responsive Tasarım**: Mobil-first, tablet ve masaüstü uyumlu
- ♿ **Erişilebilirlik**: WCAG uyumlu, ARIA etiketleri ve klavye navigasyonu
- 🎯 **Modal Detaylar**: Her uçuş için detaylı bilgi modalı
- 🧪 **Test Coverage**: Pytest ile kapsamlı otomatik testler
- 🎨 **Modern UI**: TailwindCSS ile şık ve kullanıcı dostu arayüz

## 🏗️ Teknoloji Stack

### Backend
- **Flask 3.0.0**: Python web framework
- **Jinja2**: Template motoru (Flask ile entegre)
- **Flask-WTF**: Form validasyonu
- **WTForms**: Form kütüphanesi

### Frontend
- **TailwindCSS**: Utility-first CSS framework (CDN)
- **Vanilla JavaScript**: Modal ve UI etkileşimleri
- **Jinja2 Templates**: Server-side rendering

### Geliştirme Araçları
- **pytest**: Test framework
- **pytest-flask**: Flask test yardımcıları
- **Black**: Python kod formatlayıcı
- **Flake8**: Python linter

## 📁 Dosya Yapısı

```
ucus_frontend/
├── app.py                          # Ana Flask uygulaması
├── requirements.txt                # Python bağımlılıkları
├── pyproject.toml                  # Black ve pytest konfigürasyonu
├── .flake8                         # Flake8 konfigürasyonu
├── .gitignore                      # Git ignore kuralları
├── README.md                       # Bu dosya
│
├── src/
│   ├── __init__.py
│   │
│   ├── templates/                  # Jinja2 şablonları
│   │   ├── base.html              # Ana layout
│   │   ├── index.html             # Arama sayfası
│   │   ├── flights_list.html      # Sonuç listesi
│   │   ├── flight_card.html       # Uçuş kartı partial
│   │   └── flight_detail_modal.html  # Detay modal
│   │
│   ├── static/                     # Statik dosyalar
│   │   ├── js/
│   │   │   └── ui.js              # Modal ve UI JavaScript
│   │   └── css/
│   │       └── tailwind.css       # Özel CSS (minimal)
│   │
│   ├── services/                   # İş mantığı katmanı
│   │   ├── __init__.py
│   │   └── flight_service.py      # Uçuş servisi ve mock API
│   │
│   ├── forms/                      # Form tanımlamaları
│   │   ├── __init__.py
│   │   └── search_form.py         # Arama formu validasyonu
│   │
│   ├── utils/                      # Yardımcı fonksiyonlar
│   │   ├── __init__.py
│   │   └── formatters.py          # Tarih/fiyat formatlayıcılar
│   │
│   └── tests/                      # Test dosyaları
│       ├── __init__.py
│       ├── conftest.py            # Pytest fixtures
│       ├── test_search_form.py    # Form testleri
│       ├── test_api_mock.py       # API testleri
│       ├── test_flight_list_render.py  # Render testleri
│       ├── test_modal_behavior.py # Modal testleri
│       ├── test_error_handling.py # Hata yönetimi testleri
│       └── test_formatters.py     # Formatlayıcı testleri
│
└── public/                         # Public assets (ikonlar, görseller)
```

## 🚀 Kurulum ve Çalıştırma

### Ön Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- virtualenv (önerilir)

### 1. Projeyi Klonlama
```bash
git clone https://github.com/VVuslat/ucus_frontend.git
cd ucus_frontend
```

### 2. Virtual Environment Oluşturma
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Çalıştırma
```bash
# Geliştirme modunda
python app.py

# veya Flask CLI ile
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## 🧪 Test Çalıştırma

### Tüm Testleri Çalıştırma
```bash
pytest
```

### Detaylı Çıktı ile Test
```bash
pytest -v
```

### Test Coverage Raporu
```bash
pytest --cov=src --cov-report=html
```

### Belirli Bir Test Dosyasını Çalıştırma
```bash
pytest src/tests/test_search_form.py
```

## 🎨 Kod Kalitesi

### Black ile Formatlama
```bash
black .
```

### Flake8 ile Lint Kontrolü
```bash
flake8 .
```

### Tüm Kalite Kontrolleri
```bash
black . && flake8 . && pytest
```

## 📊 API Endpoints

### Mock API Endpoints

#### GET `/api/mock/flights`
Mock uçuş verisi döndürür.

**Query Parameters:**
- `origin`: Kalkış şehri kodu (örn: IST)
- `destination`: Varış şehri kodu (örn: ESB)
- `departure_date`: Gidiş tarihi (ISO formatı)

**Response:**
```json
{
  "flights": [
    {
      "id": "FLISTESB001",
      "airline": "Turkish Airlines",
      "price": 1250.50,
      "currency": "TRY",
      "departure": "2025-10-10T08:30:00+03:00",
      "arrival": "2025-10-10T10:45:00+03:00",
      "stops": 0,
      "flightNumber": "TK123",
      "aircraft": "A320",
      "policy": "İade edilebilir"
    }
  ],
  "total": 1
}
```

#### GET `/api/flight/<flight_id>`
Tek bir uçuşun detaylı bilgilerini döndürür (JSON).

#### GET `/flight/<flight_id>/modal`
Uçuş detay modal'ının HTML içeriğini döndürür (AJAX için).

### Web Routes

#### GET `/`
Ana sayfa - arama formu

#### POST `/flights` veya GET `/flights`
Uçuş arama sonuçları sayfası

**Form/Query Parameters:**
- `origin`: Kalkış şehri (3 karakter)
- `destination`: Varış şehri (3 karakter)
- `departure_date`: Gidiş tarihi (YYYY-MM-DD)
- `return_date`: Dönüş tarihi (opsiyonel)
- `trip_type`: Yön tipi (one-way/round)
- `sort_by`: Sıralama (price/departure)
- `max_price`: Maksimum fiyat filtresi
- `stops`: Aktarma sayısı filtresi

## ✅ Kabul Kriterleri (Acceptance Criteria)

- [x] Arama formu ile istek gönderildiğinde mock API çağrısı yapılıyor
- [x] Sonuçlar `/flights` sayfasında listeleniyor
- [x] Her uçuş kartında havayolu, saatler, fiyat ve aktarma bilgisi görünüyor
- [x] Modal üzerinden ek bilgiler erişilebilir
- [x] Modal klavye ile (ESC tuşu) kapatılabiliyor
- [x] Filtre ve sıralama query parametreleri ile çalışıyor
- [x] Tüm otomatik testler `pytest` ile geçiyor (6+ test)
- [x] Responsive tasarım mobil ve masaüstünde çalışıyor
- [x] Erişilebilirlik: form etiketleri, ARIA rolleri, klavye erişimi
- [x] Black ve Flake8 ile kod kalitesi sağlanmış
- [x] README'de MYK uyumluluğu ve dosya yapısı belirtilmiş

## 🎯 MYK Yazılım Geliştirici Seviye 5 Uyumluluğu

Bu proje, MYK Yazılım Geliştirici Seviye 5 yönergesinin aşağıdaki maddelerine uygundur:

### 1. Yazılım Geliştirme Standartları
- ✅ Modüler kod yapısı (services, forms, utils, templates ayrımı)
- ✅ Tek sorumluluk prensibi (her modül kendi işini yapar)
- ✅ Temiz kod prensipleri (Black, Flake8)
- ✅ Kod dokümantasyonu (docstrings)

### 2. Test ve Kalite Güvencesi
- ✅ Otomatik test altyapısı (pytest)
- ✅ Test coverage (6+ farklı test dosyası, 50+ test case)
- ✅ Unit, integration ve functional testler
- ✅ Continuous testing yaklaşımı

### 3. Kullanıcı Arayüzü Tasarımı
- ✅ Kullanıcı deneyimi odaklı tasarım
- ✅ Responsive ve mobil uyumlu
- ✅ Erişilebilirlik standartları (WCAG)
- ✅ Hata yönetimi ve kullanıcı bildirimleri

### 4. Veri Yönetimi
- ✅ Form validasyonu (client ve server-side)
- ✅ Veri formatlama (tarih, fiyat, süre)
- ✅ API tasarımı ve dokümantasyonu

### 5. Proje Yönetimi
- ✅ Version control (Git)
- ✅ Dokümantasyon (README, docstrings)
- ✅ Bağımlılık yönetimi (requirements.txt)
- ✅ Konfigürasyon yönetimi (pyproject.toml, .flake8)

### 6. Güvenlik
- ✅ CSRF koruması (Flask-WTF)
- ✅ Input validasyonu
- ✅ XSS koruması (Jinja2 auto-escape)

## 🔄 Geliştirme İş Akışı

### Yeni Özellik Ekleme
1. Branch oluştur: `git checkout -b feature/yeni-ozellik`
2. Geliştirmeyi yap
3. Test yaz: `src/tests/test_yeni_ozellik.py`
4. Testleri çalıştır: `pytest`
5. Kod kalitesi kontrol: `black . && flake8 .`
6. Commit: `git commit -m "feat: yeni özellik açıklaması"`
7. Push ve PR oluştur

### Commit Mesajı Formatı
```
feat: yeni özellik ekleme
fix: hata düzeltme
docs: dokümantasyon güncelleme
test: test ekleme/güncelleme
refactor: kod iyileştirme
style: kod formatı düzenleme
```

### Örnek Başlangıç Commit Mesajı
```
feat(frontend): Flask tabanlı MYK uyumlu uçak bileti arama önyüzü - mock API, şablonlar, testler

- Flask + Jinja2 ile server-side rendering
- Mock API endpoint'leri (/api/mock/flights)
- WTForms ile form validasyonu
- TailwindCSS ile responsive tasarım
- Pytest ile 50+ otomatik test
- Black ve Flake8 ile kod kalitesi
- WCAG uyumlu erişilebilirlik
- Klavye ile modal kapatma
- Filtreleme ve sıralama özellikleri
```

## 📝 PR Açıklaması Şablonu

```markdown
## 🎯 Değişiklik Türü
- [ ] Yeni özellik
- [ ] Hata düzeltme
- [ ] Dokümantasyon
- [ ] Performans iyileştirme
- [ ] Test ekleme

## 📋 Açıklama
Flask + Jinja2 tabanlı, MYK Seviye 5 uyumlu uçak bileti arama frontend'i.

## ✅ Yapılanlar
- Mock API endpoint'leri
- Arama formu ve validasyon
- Responsive uçuş listesi
- Modal detay görünümü
- Filtreleme ve sıralama
- 50+ otomatik test
- Erişilebilirlik özellikleri

## 🧪 Test
- [ ] Tüm testler geçiyor (`pytest`)
- [ ] Kod formatı uygun (`black .`)
- [ ] Lint hataları yok (`flake8 .`)

## 📸 Ekran Görüntüleri
(Gerekirse ekleyin)

## 📚 İlgili Konular
Closes #issue_number
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👥 İletişim

Proje Sahibi: VVuslat
GitHub: [@VVuslat](https://github.com/VVuslat)

## 🙏 Teşekkürler

Bu proje MYK Yazılım Geliştirici Seviye 5 yönergesi doğrultusunda geliştirilmiştir.

---

**Not**: Bu proje eğitim ve demo amaçlıdır. Gerçek bir üretim ortamında kullanmadan önce güvenlik ve performans testlerinin yapılması önerilir.
