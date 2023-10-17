
import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import model
import camera
from PIL import Image

activateGui = True
threshold1 = 255/3
threshold2 = 255
kantenerkennung = False
threshholdTest = False
thresholdIterations = 20

def count_files_in_directory(directory_path):
        if os.path.exists(directory_path):
            files = os.listdir(directory_path)
            return len(files)
        else:
            return 0
        
class App:

    def __init__(self, window=tk.Tk(), window_title="Camera Classifier"): 
        self.counters = [count_files_in_directory("1"),count_files_in_directory("2"),count_files_in_directory("3")]
        self.model = model.Model(threshold1,threshold2,kantenerkennung,threshholdTest,self.counters, thresholdIterations)
        print(f" Gui applikation: {activateGui}")
        print(f" Edgedetection: {kantenerkennung}")
        print(f" Repeated Thresholdtest with {thresholdIterations} random numbers: {threshholdTest} \n")
         
        if activateGui:
            self.window = window
            self.window_title = window_title
            self.auto_predict = False
            self.camera = camera.Camera()
            self.init_gui()
            self.delay = 10 

            self.uiUpdate()
            self.window.mainloop()
        elif threshholdTest:
            self.model.testThreshholds(self.counters)
        else: 
            self.model.train_model(self.counters)
            self.model.predict_images()
    
    def init_gui(self):

        self.classname_one = "ohne"     #simpledialog.askstring("Classname One", "Enter the name of the first class:", parent=self.window)
        self.classname_two = "mit"     #simpledialog.askstring("Classname Two", "Enter the name of the second class:", parent=self.window)

        self.window.geometry("1000x700")  # Set the initial window size

        self.canvas = tk.Canvas(self.window, width=960, height=540)
        self.canvas.pack()

        control_frame = tk.Frame(self.window)
        control_frame.pack()

        buttons_frame = tk.Frame(control_frame)
        buttons_frame.pack(side=tk.LEFT, padx=20)

        toggle_frame = tk.Frame(control_frame)
        toggle_frame.pack(side=tk.LEFT, padx=20)

        train_frame = tk.Frame(control_frame)
        train_frame.pack(side=tk.LEFT, padx=20)

        input_frame = tk.Frame(control_frame)
        input_frame.pack(side=tk.LEFT, padx=20)

        self.btn_class_one = tk.Button(buttons_frame, text="Save in Trainingdata Class: " + self.classname_one, width=25, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(fill=tk.X)

        self.btn_class_two = tk.Button(buttons_frame, text="Save in Trainingdata Class: " + self.classname_two, width=25, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(fill=tk.X)

        self.btn_class_result = tk.Button(buttons_frame, text="Save in ValidationData", width=25, command=lambda: self.save_for_class(3))
        self.btn_class_result.pack(fill=tk.X)

        self.btn_train = tk.Button(train_frame, text="Train Model", width=25, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(fill=tk.X)

        self.btn_predict_validationdata = tk.Button(train_frame, text="Test Model with Validationdata", width=25, command=lambda: self.model.predict_images())
        self.btn_predict_validationdata.pack(fill=tk.X)

        self.btn_predict = tk.Button(train_frame, text="Predict current Frame", width=25, command=self.predict)
        self.btn_predict.pack(fill=tk.X)

        self.btn_toggleauto = tk.Button(toggle_frame, text=f"Toggle Auto Prediction: {self.auto_predict}", width=25, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(fill=tk.X)

        self.btn_toggleEdges = tk.Button(toggle_frame, text=f"Toggle Edgedetection: {kantenerkennung}", width=25, command=self.edges_detection_toggle)
        self.btn_toggleEdges.pack(fill=tk.X)

        self.btn_toggleThreshold = tk.Button(toggle_frame, text=f"Toggle Thresholdtest {threshholdTest}", width=25, command=self.threshold_toggle)
        self.btn_toggleThreshold.pack(fill=tk.X)

        self.class_button1 = tk.Button(input_frame, text=f"Threshold1: {threshold1}", width=25, command=lambda:self.switch_threshold(1))
        self.class_button1.pack(fill=tk.X)

        self.class_button2 = tk.Button(input_frame, text=f"Threshold2: {threshold2}", width=25, command=lambda:self.switch_threshold(2))
        self.class_button2.pack(fill=tk.X)

        self.class_button4 = tk.Button(input_frame, text=f"Iterations: {thresholdIterations}", width=25, command=lambda:self.switch_thresholdIteration())
        self.class_button4.pack(fill=tk.X)

        self.class_label3 = tk.Label(self.window, text="Results Here!", font=("Arial", 15))
        self.class_label3.pack(fill=tk.X)

    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict

    def edges_detection_toggle(self):
        global kantenerkennung
        kantenerkennung = not kantenerkennung

    def threshold_toggle(self):
        global threshholdTest
        threshholdTest = not threshholdTest
        
    def switch_thresholdIteration(self):
        global thresholdIterations
        thresholdIterations =  simpledialog.askinteger("Threshold iterations", "Enter how many Random Thresholds should be tested:", parent=self.window)
    
    def switch_threshold(self,number):
        global threshold1
        global threshold2
        if number == 1:
            threshold1 = simpledialog.askinteger("Threshold1", "Enter the first Threshold:", parent=self.window)
        elif number == 2:
            threshold2 = simpledialog.askinteger("Threshold2", "Enter the second Threshold:", parent=self.window)
        
        if kantenerkennung:     
            messagebox.showinfo("Notice", "You need to Train the model again!")

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")
        if not os.path.exists("3"):
            os.mkdir("3")
        
        cv.imwrite(f'{class_num}/frame{self.counters[class_num-1]}.jpg',frame)
        img = PIL.Image.open(f'{class_num}/frame{self.counters[class_num - 1]}.jpg')
        img.thumbnail((500, 282), resample=Image.LANCZOS)
        img.save(f'{class_num}/frame{self.counters[class_num - 1]}.jpg')
        self.counters[class_num - 1] += 1

    def reset(self):
        for folder in ['1', '2']:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        self.counters = [1, 1]
        self.model = model.Model()
        self.class_label.config(text="CLASS")

    def uiUpdate(self):
        if self.auto_predict:
            print(self.predict())

        ret, frame = self.camera.get_frame()
        if ret:
            frame = cv.resize(frame, (960, 540))
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            image=PIL.Image.fromarray(frame)
           
            if kantenerkennung:
                image.save("frameedges.jpg")
                image = cv.imread('frameedges.jpg')[:, :, 0]
                edges = cv.Canny(image, threshold1=threshold1, threshold2=threshold2)
                image = PIL.Image.fromarray(edges, mode="L")  # Konvertiere zu Graustufenbild

            self.photo = PIL.ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.class_button1.config(text=f"Threshold1: {threshold1}")
        self.class_button2.config(text=f"Threshold2: {threshold2}")
        self.class_button4.config(text=f"Iterations: {thresholdIterations}")
        self.btn_toggleThreshold.config(text=f"Toggle Thresholdtest {threshholdTest}")
        self.btn_toggleEdges.config(text=f"Toggle Edgedetection: {kantenerkennung}")
        self.btn_toggleauto.config(text=f"Toggle Auto Prediction: {self.auto_predict}")
        self.window.after(self.delay, self.uiUpdate)

    def predict(self):
        ret, frame = self.camera.get_frame()
        if ret:
            prediction = self.model.predict_live(frame)

        if prediction == 1:
            self.class_label3.config(text=self.classname_one)
            return self.classname_one
        if prediction == 2:
            self.class_label3.config(text=self.classname_two)
            return self.classname_two
        
    