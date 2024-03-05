import cv2
import numpy as np
from imageToWordModel import ImageToWordModel
import pandas as pd
from tqdm import tqdm
from config import ModelConfigs




if __name__ == "__main__":


    config = ModelConfigs.load("Models/202403051356/configs.yaml")

    model = ImageToWordModel(model_path=config.model_path, char_list=config.vocab)

    df = pd.read_csv("Models/202403051356/val.csv").values.tolist()

    accum_cer = []
    for image_path, label in tqdm(df):
        image = cv2.imread(image_path)

        prediction_text = model.predict(image)

        cer = model.get_cer(prediction_text, label)

        print(f"Image: {image_path}, Label: {label}, Prediction: {prediction_text}, Cer: {cer}")
    

        accum_cer.append(cer)

    print(f"Average CER: {np.average(accum_cer)}")