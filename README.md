# ✈️ Uçuş Arama - Flight Search Application

Bu uygulama sayesinde gitmek istediğiniz bölgeyi girdiğinizde bu bölgeye giden en uygun fiyatlı uçak biletini görüntüleyebilirsiniz.

## 🚀 Özellikler

- **Uçuş Arama**: Kalkış, varış noktası ve tarih seçerek uçuş arama
- **Sonuç Listeleme**: Fiyat, saat ve havayolu bilgisi ile uçuşları kartlarda görüntüleme
- **Detaylı Bilgi**: Modal pencerede uçuş detaylarını (bagaj, iptal politikası, ikramlar) görüntüleme
- **Responsive Tasarım**: Mobil, tablet ve masaüstü cihazlarda uyumlu görünüm
- **Modern UI**: Tailwind CSS ile tasarlanmış kullanıcı dostu arayüz
- **Mock API**: Test için hazır mock veri servisi

## 📋 Gereksinimler

- Node.js (v18 veya üzeri)
- npm (v9 veya üzeri)

## 🔧 Kurulum

1. **Depoyu Klonlayın**
```bash
git clone https://github.com/VVuslat/ucus_frontend.git
cd ucus_frontend
```

2. **Bağımlılıkları Yükleyin**
```bash
npm install
```

3. **Geliştirme Sunucusunu Başlatın**
```bash
npm run dev
```

Uygulama `http://localhost:5173` adresinde çalışacaktır.

## 🧪 Testler

Testleri çalıştırmak için:

```bash
npm test
```

Test kapsamı:
- Uygulama bileşeni testleri
- Arama formu testleri
- Uçuş kartı testleri

## 🏗️ Build

Production build oluşturmak için:

```bash
npm run build
```

Build dosyaları `dist` klasöründe oluşturulacaktır.

Build'i önizlemek için:

```bash
npm run preview
```

## 📦 Proje Yapısı

```
ucus_frontend/
├── src/
│   ├── components/          # React bileşenleri
│   │   ├── SearchForm.jsx   # Arama formu
│   │   ├── FlightList.jsx   # Uçuş listesi
│   │   ├── FlightCard.jsx   # Uçuş kartı
│   │   └── Modal.jsx        # Detay modal
│   ├── services/            # API servisleri
│   │   └── flightService.js # Mock uçuş API
│   ├── test/                # Test dosyaları
│   │   ├── App.test.jsx
│   │   ├── SearchForm.test.jsx
│   │   ├── FlightCard.test.jsx
│   │   └── setup.js
│   ├── App.jsx              # Ana uygulama
│   ├── main.jsx             # Giriş noktası
│   └── index.css            # Global stiller
├── public/                  # Statik dosyalar
├── package.json
├── vite.config.js          # Vite yapılandırması
├── vitest.config.js        # Test yapılandırması
├── tailwind.config.js      # Tailwind yapılandırması
└── README.md
```

## 🎨 Teknolojiler

- **React 19**: UI framework
- **Vite**: Build tool ve dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Vitest**: Test framework
- **React Testing Library**: React bileşen testleri

## 💡 Kullanım

1. **Uçuş Arama**:
   - "Nereden" alanına kalkış şehrini girin
   - "Nereye" alanına varış şehrini girin
   - Tarih seçin
   - "Uçuş Ara" butonuna tıklayın

2. **Sonuçları İnceleme**:
   - Arama sonuçları kartlar halinde listelenir
   - Her kartta havayolu, uçuş saatleri ve fiyat bilgisi görünür

3. **Detayları Görüntüleme**:
   - Herhangi bir kartın "Detaylar" butonuna tıklayın
   - Modal pencerede bagaj hakkı, iptal politikası ve ikramlar görüntülenir
   - Modal'ı kapatmak için "Kapat" butonuna veya dışarıya tıklayın

## 🖼️ Ekran Görüntüleri

### Ana Sayfa
![Ana Sayfa](https://github.com/user-attachments/assets/8b1538f4-3a82-49c8-8974-43cd35cd948b)

### Arama Sonuçları
![Arama Sonuçları](https://github.com/user-attachments/assets/ba7e6cc9-a533-47f0-bf87-639a0d832cd0)

### Uçuş Detayları
![Uçuş Detayları](https://github.com/user-attachments/assets/ee7b2e80-e956-40e5-a553-9ec0f6b84e08)

### Mobil Görünüm
![Mobil Görünüm](https://github.com/user-attachments/assets/61f60545-81c1-440b-aeea-8f6b403e5ac2)

## 🛠️ Geliştirme

Kod kalitesini kontrol etmek için:

```bash
npm run lint
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
