from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
from PIL import Image
import os
import random
class Model:
    counters = -1
    threshold1 = -1
    threshold2 = -1
    kantenerkennung = False
    threshholdTest = False
    thresholdIterations = 0
    dateiname = ""

    def __init__(self, threshold1, threshold2, kantenerkennung, thresholdtest, counters, thresholdIterations):
        self.model = LinearSVC(dual=True)
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.threshholdTest= thresholdtest
        self.kantenerkennung = kantenerkennung
        self.counters = counters
        self.thresholdIterations = thresholdIterations

    def testThreshholds(self, counters):
        best_accuracy = 0
        best_threshold = [-1,-1]
        
        threshold_values = [(random.randint(50, 200), random.randint(100, 500)) for _ in range(self.thresholdIterations)]
        print(f"Random generated Thresholds: {threshold_values}")
        for threshold in threshold_values:
            self.threshold1 = threshold[0]
            self.threshold2 = threshold[1]
            print(f"\nusing T1: {self.threshold1} T2:{self.threshold2}")
            self.train_model(counters)
            
            result = self.predict_images()
            if result[2] > best_accuracy:
                best_accuracy = result[2]
                best_threshold = (result[0], result[1])
            os.rename(self.dateiname,os.path.splitext(self.dateiname)[0]+"_acc_"+str(round(result[2],2))+".txt")
        print(f"Best Accurancy: {best_accuracy}\nBest Thresholds 1: {best_threshold[0]} 2: {best_threshold[1]}")
        

    def predict_images(self):
        prediction_results = []
        counter1 = 0
        counter2 = 0
        accuracycounter = 0
        self.dateiname = "./results/result"
        if(self.kantenerkennung):
            self.dateiname += "_"+str(self.threshold1)+"_"+str(self.threshold2)+".txt"
        else:
            self.dateiname += ".txt"

        if not os.path.exists(self.dateiname):
            print("\rStarting predicting validationdata!")
            with open(self.dateiname, 'w') as f:
                for file_name in os.listdir('3'):
                    img_path = os.path.join('3', file_name)
                    img = Image.open(img_path)
                    img.thumbnail((500, 282), resample=Image.LANCZOS)
                    img.save(img_path)
                    img = cv.imread(img_path)[:, :, 0]
                    img = img.reshape(140500)

                    # Führen Sie die Kantenerkennung durch
                    if self.kantenerkennung:
                        img = cv.Canny(img, threshold1=self.threshold1, threshold2=self.threshold2)  # Die Schwellenwerte können angepasst werden
                        img = img.flatten()
                    

                    prediction = self.model.predict([img])[0]

                    # Check if the prediction matches the "Ohne" or "Schlagloch" prefix in the filename
                    if (prediction == 1 and file_name.startswith("Ohne")) or (prediction == 2 and file_name.startswith("Schlagloch")):
                        accuracycounter += 1
                
                    # Schreibe das Ergebnis in die Ergebnisdatei
                    if prediction == 1:
                        counter1 += 1
                    elif prediction == 2:
                        counter2 += 1

                    result_line = f"{file_name} : {prediction}\n"
                    f.write(result_line)

                    prediction_results.append((img_path, prediction))

                f.write(f"\nClass1: {counter1} Class2: {counter2} \nModel Accurancy: {accuracycounter/(counter1+counter2) *100}%")
                print("\rFinished predicting validationdata! \nModel Accurancy: " + str(accuracycounter/(counter1+counter2) *100) +"%")

                if self.threshholdTest:
                    return [self.threshold1,self.threshold2,accuracycounter/(counter1+counter2) *100]
            os.rename(self.dateiname,os.path.splitext(self.dateiname)[0]+"_acc_"+str(round(accuracycounter/(counter1+counter2) *100,2))+".txt")
            return prediction_results
        else:  
            print("\rResults with this Thresholds already exists in Results")

    def train_model(self, counters):
        img_list = np.array([])
        class_list = np.array([])

        if self.kantenerkennung:
            print(f"Using Threshold 1: {self.threshold1} Threshold 2: {self.threshold2}")
            
        for i in range(1, counters[0]):
            img = cv.imread(f'1/frame{i}.jpg')[:, :, 0]
            img = img.reshape(140500)
            # Führen Sie die Kantenerkennung durch
            if self.kantenerkennung:
                img = cv.Canny(img, threshold1=self.threshold1, threshold2=self.threshold2)  # Die Schwellenwerte können angepasst werden
                img = img.flatten()
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 1)

            if i % 10 == 0:
                percentage = int(i / counters[0] * 100)
                print(f"\rLoad Class1 pictures: {percentage}%", end='', flush=True)
        print("")
        for i in range(1, counters[1]):
            img = cv.imread(f'2/frame{i}.jpg')[:, :, 0]
            img = img.reshape(140500)
            # Führen Sie die Kantenerkennung durch
            if self.kantenerkennung:
                img = cv.Canny(img, threshold1=self.threshold1, threshold2=self.threshold2)  # Die Schwellenwerte können angepasst werden
                img = img.flatten()
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 2)
            if i % 10 == 0:
                percentage = int(i / counters[1] * 100)
                print(f"\rLoad Class2 pictures: {percentage}%", end='', flush=True)
                
        print("\nStart reshape Model...")
        img_list = img_list.reshape(self.counters[0]-1 + self.counters[1]-1, 140500)
        print("Start training Model...")
        self.model.fit(img_list, class_list)
        print("Model successfully trained!")

    def predict_live(self, frame):

        cv.imwrite("frame.jpg", frame)
        img = Image.open("frame.jpg")
        img.thumbnail((500, 282), resample=Image.LANCZOS)
        img.save("frame.jpg")
        
        img = cv.imread('frame.jpg')[:, :, 0]
        img = img.reshape(140500)
        # Führen Sie die Kantenerkennung durch
        if self.kantenerkennung:
            img = cv.Canny(img, threshold1=self.threshold1, threshold2=self.threshold2)  # Die Schwellenwerte können angepasst werden
            img = img.flatten()
        prediction = self.model.predict([img])

        return prediction[0]
    

    