import cv2
import numpy as np

threshold1 = 255/3
threshold2 = 255

# Laden Sie das Bild
image = cv2.imread(r'.\3\Ohne9.jpg', 0)  # Laden Sie das Bild in Graustufen
image2 = cv2.imread(r'.\3\Schlagloch10.jpg', 0)  # Laden Sie das Bild in Graustufen
# Führen Sie die Kantenerkennung durch
edges = cv2.Canny(image, threshold1=threshold1, threshold2=threshold2)  # Die Schwellenwerte können angepasst werden
edges2 = cv2.Canny(image2, threshold1=threshold1, threshold2=threshold2)  # Die Schwellenwerte können angepasst werden

# Zeigen Sie das Originalbild und das Ergebnis der Kantenerkennung an
cv2.imshow('Original Image mit', image2)
cv2.imshow('Edges mit', edges2)
cv2.imshow('Original Image Ohne', image)
cv2.imshow('Edges Ohne', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
