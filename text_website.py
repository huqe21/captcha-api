from flask import Flask, request, render_template_string, url_for, send_from_directory, session
import os
import random
import uuid  # Importiere die UUID-Bibliothek
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = 'eine_sehr_geheime_schluessel'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

CAPTCHA_FOLDER = '/Users/hugoniescken/Desktop/ki/captchaSolver/captcha-api/Dataset'

def load_captcha_images():
    captcha_files = os.listdir(CAPTCHA_FOLDER)
    return {file.rsplit('.', 1)[0]: file for file in captcha_files}

captcha_images = load_captcha_images()

@app.route('/captcha_image/<filename>')
@cross_origin()

def captcha_image(filename):
    secure_file = secure_filename(filename)
    return send_from_directory(CAPTCHA_FOLDER, secure_file)

@app.route('/')
@cross_origin()
def home():
    captcha_answer, captcha_filename = random.choice(list(captcha_images.items()))
    session['captcha_answer'] = captcha_answer
    captcha_url = url_for('captcha_image', filename=captcha_filename)
    # Generiere eine einzigartige ID für das CAPTCHA-Bild
    captcha_id = str(uuid.uuid4())
    form_html = f'''
    <html>
        <head><title>CAPTCHA-Beispiel</title></head>
        <body>
            <p>Bitte geben Sie den Text des CAPTCHA-Bildes ein:</p>
            <form action="/validate" method="post">
                <div><img src="{captcha_url}" alt="CAPTCHA" id="{captcha_id}"></div>
                <input type="hidden" name="captcha_id" value="{captcha_id}">
                <input type="text" name="captcha_user" placeholder="CAPTCHA eingeben">
                <input type="submit" value="Einreichen">
            </form>
        </body>
    </html>
    '''
    return render_template_string(form_html)

@app.route('/validate', methods=['POST'])
@cross_origin()
def validate_captcha():
    correct_answer = session.get('captcha_answer', '')
    user_input = request.form.get('captcha_user', '').strip()
    
    if correct_answer == user_input:
        return '<p>CAPTCHA erfolgreich validiert!</p>'
    else:
        return '<p>Ungültiges CAPTCHA. Bitte versuchen Sie es erneut.</p>'

if __name__ == '__main__':
    app.run(debug=True, port=5555)
