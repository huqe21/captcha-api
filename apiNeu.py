from flask import Flask, request
from flask_cors import CORS
from config import ModelConfigs
from imageToWordModel import ImageToWordModel
import cv2
import os
from apiConfig import Config


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

configs = ModelConfigs.load("Models/202403051356/configs.yaml")

model = ImageToWordModel(model_path=configs.model_path, char_list=configs.vocab)

client = MongoClient(Config.MONGO_URI)
db = client['valid8users']
users_collection = db ['users']


@app.route('/captcha-solver', methods=['POST'])
def solve_captcha():
    json = ""
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
    
    
