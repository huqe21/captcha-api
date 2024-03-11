// Findet das CAPTCHA-Bild auf der Seite
const captchaImage = document.querySelector('img[alt="CAPTCHA"]');
// Annahme, dass das Antwortfeld ein Input-Feld mit einem spezifischen Namen oder ID ist
const captchaInputField = document.querySelector('input[name="captcha_user"]'); 

if (captchaImage && captchaInputField) {
    // Versucht, das Bild als Blob zu holen
    fetch(captchaImage.src)
    .then(response => response.blob())
    .then(blob => {
        // Extrahiert den Dateinamen aus der Bild-URL
        const imageUrl = new URL(captchaImage.src);
        const pathname = imageUrl.pathname;
        const filename = pathname.split('/').pop(); // Extrahiert den Dateinamen aus dem Pfad

        const formData = new FormData();
        formData.append('file', blob, filename); 

        // Sendet das Bild zur Flask-API
        fetch('http://127.0.0.1:5000/captcha-solver', { 
            method: 'POST',
            body: formData, // Sendet das Bild als FormData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Netzwerkantwort war nicht ok');
            }
            return response.json();
        })
        .then(data => {
            
            captchaInputField.value = data.captcha;
        })
        .catch(error => console.error('Error:', error));
    });
}
