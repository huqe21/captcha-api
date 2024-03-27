import stow
import os
import cv2


folder_path = "captcha_dataset"

if __name__ == "__main__":
    for file in stow.ls(folder_path):
            # Lade das Bild
            image_path = os.path.join(folder_path, file)
            image = cv2.imread(image_path)

            # Konvertiere das Bild in Schwarzweiß
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Speichere das Schwarzweiß-Bild mit einem Präfix "bw_"
            bw_image_path = os.path.join('Dataset', file)
            cv2.imwrite(bw_image_path, gray_image)