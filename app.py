
import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import model
import camera
from PIL import Image

def count_files_in_directory(directory_path):
        if os.path.exists(directory_path):
            files = os.listdir(directory_path)
            return len(files)
        else:
            return 0
        

activateGui = True
threshold1 = 100/2
threshold2 = 100
kantenerkennung = True
threshholdTest = False
thresholdIterations = 20

class App:

    def __init__(self, window=tk.Tk(), window_title="Camera Classifier"):

       
        self.counters = [count_files_in_directory("1"),count_files_in_directory("2"),count_files_in_directory("3")]
        self.model = model.Model(threshold1,threshold2,kantenerkennung,threshholdTest,self.counters, thresholdIterations)
        print(f" Edgedetection: {kantenerkennung}")
        print(f" Repeated Thresholdtest with {thresholdIterations} random numbers: {threshholdTest} \n")
        
        
        if activateGui:
            self.window = window
            self.window_title = window_title
            self.auto_predict = False
            self.camera = camera.Camera()
            self.init_gui()
            self.delay = 15
            self.update()
            self.window.mainloop()
        elif threshholdTest:
            self.model.testThreshholds(self.counters)
        else: 
            self.model.train_model(self.counters)
            self.model.predict_images()
    
    def init_gui(self):

        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        #if kantenerkennung:
        #    self.canvas_edges = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        #    self.canvas_edges.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.classname_one = "ohne"     #simpledialog.askstring("Classname One", "Enter the name of the first class:", parent=self.window)
        self.classname_two = "mit"     #simpledialog.askstring("Classname Two", "Enter the name of the second class:", parent=self.window)
        

        self.btn_class_one = tk.Button(self.window, text="Save in Trainingdata Class: "+ self.classname_one, width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_two = tk.Button(self.window, text="Save in Trainingdata Class: "+ self.classname_two, width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_result = tk.Button(self.window, text="Save in ValidationData", width=50, command=lambda: self.save_for_class(3))
        self.btn_class_result.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predcit", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict_validationdata = tk.Button(self.window, text="Predict Validationdata", width=50, command=lambda: self.model.predict_images())
        self.btn_predict_validationdata.pack(anchor=tk.CENTER, expand=True)
        #self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        #self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)

    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict

    def edges_detection_toggle():
        kantenerkennung = not kantenerkennung

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

    def update(self):
        if self.auto_predict:
            print(self.predict())

        ret, frame = self.camera.get_frame()

        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            image=PIL.Image.fromarray(frame)
            #image.thumbnail((500, 282), resample=Image.LANCZOS)
            self.photo = PIL.ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        #if kantenerkennung:
        #    self.canvas_edges.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        ret, frame = self.camera.get_frame()
        if ret:
            prediction = self.model.predict_live(frame)

        if prediction == 1:
            self.class_label.config(text=self.classname_one)
            return self.classname_one
        if prediction == 2:
            self.class_label.config(text=self.classname_two)
            return self.classname_two
        
    