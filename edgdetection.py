import cv2 as cv
import os

def kantenerkennung_und_speichern(input_folder, output_folder):
    # Erstelle das Ausgabeverzeichnis, falls es nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print("created outputfolder.")


    # Liste alle Dateien im Eingabeverzeichnis auf
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Nur Bilddateien
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Lade das Bild
           # image = cv.imread(input_path)

            # Kanten mit Canny-Detektor erkennen
            gray = cv.imread(input_path)[:, :, 0]#cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, threshold1=100, threshold2=200)

            # Speichere das bearbeitete Bild
            cv.imwrite(output_path, edges)

            print(f"Kanten von {input_path} wurden erkannt und in {output_path} gespeichert.")

# Verwende die Funktion, um Kanten in Bildern zu erkennen und sie in einem Ausgabeverzeichnis zu speichern
input_folder = "2"  # Passe den Pfad an
output_folder = "AusgabeVerzeichnis2"  # Passe den Pfad an
kantenerkennung_und_speichern(input_folder, output_folder)
