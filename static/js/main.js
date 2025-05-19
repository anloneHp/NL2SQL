document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('translationForm');
    const resultDiv = document.getElementById('result');
    const sqlOutput = document.getElementById('sql_output');
    const copyBtn = document.getElementById('copyBtn');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const inputText = document.getElementById('input_text').value.trim();
        if (!inputText) {
            alert('Lütfen bir metin girin');
            return;
        }

        // Yükleniyor mesajı
        resultDiv.classList.remove('hidden');
        sqlOutput.textContent = 'İşleniyor, lütfen bekleyin...';
        
        // Butonu devre dışı bırak
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'İşleniyor...';

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'input_text=' + encodeURIComponent(inputText)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            sqlOutput.textContent = data.sql_query || 'Sonuç bulunamadı';
        })
        .catch(error => {
            console.error('Hata:', error);
            sqlOutput.textContent = 'Bir hata oluştu: ' + (error.message || 'Bilinmeyen hata');
        })
        .finally(() => {
            // Butonu tekrar aktif et
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
        });
    });

    
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const textToCopy = sqlOutput.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                
                const originalText = copyBtn.textContent;
                copyBtn.textContent = 'Kopyalandı!';
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Kopyalama hatası:', err);
                alert('Kopyalama işlemi başarısız oldu');
            });
        });
    }
});