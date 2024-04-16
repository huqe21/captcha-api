const API_KEY = "AIzaSyDm62QMTfDr_aVoUZO58KeYFYg8nZYEvwE"

let userSignedIn = false;

// Findet das CAPTCHA-Bild auf der Seite
const captchaImage = document.querySelector('img[alt="CAPTCHA"]');
// Annahme, dass das Antwortfeld ein Input-Feld mit einem spezifischen Namen oder ID ist
const captchaInputField = document.querySelector('input[name="captcha_user"]'); 


if (captchaImage && captchaInputField) {
    // Versucht, das Bild als Blob zu holen
    fetch(captchaImage.src)
    .then(response => response.blob())
    .then(async blob => {
        // Extrahiert den Dateinamen aus der Bild-URL
        const imageUrl = new URL(captchaImage.src);
        const pathname = imageUrl.pathname;
        const filename = pathname.split('/').pop(); // Extrahiert den Dateinamen aus dem Pfad
        let tokenVal = "";
        await chrome.runtime.sendMessage({type: "getAuthToken"}, function(response) {
            tokenVal = response.token;
        });

        const formData = new FormData();
        formData.append('file', blob, filename); 

        // Sendet das Bild zur Flask-API
        fetch('http://127.0.0.1:5000/captcha-solver', { 
            method: 'POST',
            headers: {
                token: tokenVal
            },
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
