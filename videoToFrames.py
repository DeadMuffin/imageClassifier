import cv2

# Video-Datei öffnen
video_path = 'test.mp4'
cap = cv2.VideoCapture(video_path)

# Stelle sicher, dass das Video erfolgreich geöffnet wurde
if not cap.isOpened():
    print("Fehler beim Öffnen der Video-Datei")
    exit()

frame_count = 0
frame_interval = 10  # Speichere jedes 10. Frame

# Verzeichnis erstellen, um die Frames zu speichern
output_directory = 'Videoframes'
import os
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Schleife durch das Video und speichere Frames
while True:
    ret, frame = cap.read()

    if not ret:
        break

    if frame_count % frame_interval == 0:
        # Speichere den Frame im Verzeichnis
        frame_filename = f'{output_directory}/frame_{frame_count:04d}.jpg'
        cv2.imwrite(frame_filename, frame)

    frame_count += 1

# Video-Datei schließen
cap.release()

print(f"{frame_count} Frames wurden gespeichert (jedes {frame_interval}. Frame).")
