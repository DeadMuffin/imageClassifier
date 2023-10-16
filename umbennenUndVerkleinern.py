import os
import cv2
from PIL import Image

# Verzeichnis, das du durchsuchen möchtest
verzeichnis = os.getcwd()

# Liste aller Dateien im Verzeichnis
dateien = [datei for datei in os.listdir(verzeichnis) if datei.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Sortiere die Dateien nach ihrem Namen
dateien.sort()

# Laufvariable für die Nummer des aktuellen Rahmens
frame_nummer = 1

# prefix für jede Datei
prefix = "Frame"


# Schleife zum Umbenennen und Verkleinern der Dateien
for datei in dateien:
    # Erzeuge den neuen Dateinamen
    neuer_dateiname = f"{prefix}{frame_nummer}.jpg"
    
    # Voller Pfad zur aktuellen Datei
    alter_pfad = os.path.join(verzeichnis, datei)
    
    # Voller Pfad zum neuen Dateinamen
    neuer_pfad = os.path.join(verzeichnis, neuer_dateiname)
    
    # Umbenennen der Datei
    os.rename(alter_pfad, neuer_pfad)

    # Öffne das Bild und verkleinere es
    img = Image.open(neuer_pfad)
    img.thumbnail((500, 282), resample=Image.LANCZOS)
    img.save(neuer_pfad)

    # Inkrementiere die Frame-Nummer für die nächste Datei
    frame_nummer += 1

print("Umbenennung und Verkleinerung abgeschlossen.")
