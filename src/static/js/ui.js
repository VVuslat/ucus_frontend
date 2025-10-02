/**
 * UI etkileşimleri - modal, klavye kapatma ve diğer küçük DOM manipülasyonları.
 * Vanilla JavaScript ile yazılmıştır.
 */

/**
 * Modal açma fonksiyonu - uçuş detaylarını AJAX ile yükler.
 * @param {string} flightId - Uçuş ID'si
 */
function openFlightModal(flightId) {
    const modalContainer = document.getElementById('modal-container');
    const modalContent = document.getElementById('modal-content');
    
    // Modal'ı göster
    modalContainer.classList.remove('hidden');
    modalContainer.setAttribute('aria-hidden', 'false');
    
    // Loading state
    modalContent.innerHTML = `
        <div class="p-12 text-center">
            <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
            <p class="text-gray-600">Uçuş detayları yükleniyor...</p>
        </div>
    `;
    
    // AJAX ile modal içeriğini yükle
    fetch(`/flight/${flightId}/modal`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Uçuş bulunamadı');
            }
            return response.text();
        })
        .then(html => {
            modalContent.innerHTML = html;
            // İlk focusable elemente odaklan (erişilebilirlik)
            const firstFocusable = modalContent.querySelector('button, a, input, select, textarea');
            if (firstFocusable) {
                firstFocusable.focus();
            }
        })
        .catch(error => {
            modalContent.innerHTML = `
                <div class="p-12 text-center">
                    <div class="text-red-500 text-5xl mb-4">⚠️</div>
                    <h3 class="text-xl font-semibold text-gray-800 mb-2">Hata</h3>
                    <p class="text-gray-600 mb-4">${error.message}</p>
                    <button onclick="closeModal()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">
                        Kapat
                    </button>
                </div>
            `;
        });
}

/**
 * Modal kapatma fonksiyonu.
 */
function closeModal() {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.add('hidden');
    modalContainer.setAttribute('aria-hidden', 'true');
    
    // İçeriği temizle
    const modalContent = document.getElementById('modal-content');
    modalContent.innerHTML = '';
}

/**
 * Sayfa yüklendiğinde event listener'ları ekle.
 */
document.addEventListener('DOMContentLoaded', function() {
    const modalContainer = document.getElementById('modal-container');
    const modalBackdrop = document.getElementById('modal-backdrop');
    
    // Modal backdrop'a tıklandığında kapat
    if (modalBackdrop) {
        modalBackdrop.addEventListener('click', closeModal);
    }
    
    // ESC tuşu ile modal'ı kapat - erişilebilirlik
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' || event.key === 'Esc') {
            const modalContainer = document.getElementById('modal-container');
            if (!modalContainer.classList.contains('hidden')) {
                closeModal();
            }
        }
    });
    
    // Form inputlarında ENTER tuşu ile submit önleme (gerekirse)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('keydown', function(event) {
            // Sadece text input'larda ENTER ile submit'i engelle
            if (event.key === 'Enter' && event.target.tagName === 'INPUT' && event.target.type === 'text') {
                // Default davranışı engelleme - form submit olmasın
                // Bu durumda explicit submit butonu kullanılmalı
            }
        });
    });
});

/**
 * Smooth scroll fonksiyonu - sayfa içi navigasyon için.
 * @param {string} elementId - Hedef element ID'si
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Toast bildirimi gösterme fonksiyonu (isteğe bağlı kullanım için).
 * @param {string} message - Gösterilecek mesaj
 * @param {string} type - Bildirim tipi ('success', 'error', 'info')
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 fade-in`;
    
    // Tip'e göre renk
    if (type === 'success') {
        toast.className += ' bg-green-500 text-white';
    } else if (type === 'error') {
        toast.className += ' bg-red-500 text-white';
    } else {
        toast.className += ' bg-blue-500 text-white';
    }
    
    toast.textContent = message;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    
    document.body.appendChild(toast);
    
    // 3 saniye sonra kaldır
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Global fonksiyonları window objesine ekle
window.openFlightModal = openFlightModal;
window.closeModal = closeModal;
window.smoothScrollTo = smoothScrollTo;
window.showToast = showToast;
