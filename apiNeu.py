from flask import Flask, request
from flask_cors import CORS
from config import ModelConfigs
from imageToWordModel import ImageToWordModel
import cv2
import os
from pymongo import MongoClient
import requests


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

configs = ModelConfigs.load("Models/202403051356/configs.yaml")

model = ImageToWordModel(model_path=configs.model_path, char_list=configs.vocab)

CONNECTION_STRING = 'mongodb+srv://luca:281201@aiducate.ov1kgw7.mongodb.net/test'

client = MongoClient(CONNECTION_STRING)
db = client.test
users_collection = db.users


def validate_email_in_database(email):
    return users_collection.find_one({'email': email})

def validate_and_decode_google_token(token):
    userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    
    # Header für die Anfrage, einschließlich des Access Tokens
    headers = {'Authorization': f'Bearer {token}'}

    # Führe den GET-Request aus
    response = requests.get(userinfo_url, headers=headers)

    # Überprüfe den Status-Code der Antwort
    if response.status_code == 200:
        # Anfrage war erfolgreich, parse die Antwort als JSON
        user_info = response.json()
        return user_info
    else:
        # Es gab ein Problem mit der Anfrage
        print(f"Failed to retrieve user info, status code: {response.status_code}")
        return None
    
@app.route('/authorize-user', methods= ['GET'])
def authorize_user():
    tokenVal = request.headers.get('token')

    user_info = validate_and_decode_google_token(tokenVal)

    if user_info is None or 'email' not in user_info:
        return 'Unable to fetch user info from Google API', 401

    email_from_google = user_info['email']
    
    if not validate_email_in_database(email_from_google):
        return 'Email not found in database', 401
    return {},200
                      

@app.route('/captcha-solver', methods=['POST'])
def solve_captcha():

    tokenVal = request.headers.get('token')

    user_info = validate_and_decode_google_token(tokenVal)

    if user_info is None or 'email' not in user_info:
        return 'Unable to fetch user info from Google API', 401

    email_from_google = user_info['email']
    
    if not validate_email_in_database(email_from_google):
        return 'Email not found in database', 401
   
    json =  ""
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        image = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))
        prediction = model.predict(image)
        json = {'captcha': str(prediction)}

    if os.path.exists(os.path.join(UPLOAD_FOLDER, file.filename)):
        os.remove(os.path.join(UPLOAD_FOLDER, file.filename))

    return json, 200

if __name__ == '__main__':
    app.run(debug=False)
    
    
