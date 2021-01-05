from tkinter import *
import math
import time
import tensorflow as tf
import numpy as np

class App():

    def replaceBoxWithFilled(self, xBoxLoc, yBoxLoc, add=0.10):
            self.fill[xBoxLoc][yBoxLoc] = min(self.fill[xBoxLoc][yBoxLoc] + add, 1)
            color = '#' + f'{int(255 * (1.0 - self.fill[xBoxLoc, yBoxLoc])):x}' * 3
            if color == '# 0 0 0':
                color = '#000000'
            self.canvas.delete(self.squares[xBoxLoc][yBoxLoc])
            self.squares[xBoxLoc][yBoxLoc] = self.canvas.create_rectangle(xBoxLoc * self.sq_size, yBoxLoc * self.sq_size,
                                                           xBoxLoc * self.sq_size + self.sq_size, yBoxLoc * self.sq_size + self.sq_size, fill=color)

    def draw(self, event):
        boxx = event.x // self.sq_size
        boxy = event.y // self.sq_size

        boxx = max(0, min(boxx, self.resolution - 1))
        boxy = max(0, min(boxy, self.resolution - 1))

        self.replaceBoxWithFilled(boxx, boxy)
        self.replaceBoxWithFilled(max(boxx - 1, 0), boxy)
        self.replaceBoxWithFilled(min(boxx + 1, self.resolution - 1), boxy)
        self.replaceBoxWithFilled(boxx, max(boxy - 1, 0))
        self.replaceBoxWithFilled(boxx, min(boxy + 1, self.resolution - 1))

    def release(self, event):

        array = np.resize(self.fill, (1, 28, 28))
        resultNumber = np.argmax(self.Model.predict(array.reshape(1, 28, 28)), axis=1)
        print(resultNumber)

    def reset(self, event):
        print("Resetting...")

        for i in range(self.resolution):
            for j in range(self.resolution):
                self.canvas.delete(self.squares[i][j])

        for i in range(self.resolution):
            for j in range(self.resolution):
                self.squares[i][j] = self.canvas.create_rectangle(i * self.sq_size, j * self.sq_size, i * self.sq_size + self.sq_size, j * self.sq_size + self.sq_size, fill = 'white')

        self.fill = np.zeros((self.resolution,self.resolution))

    def __init__(self, master):
        # self.playing = Falses
        self.cur = time.time()

        self.resolution = 28
        self.sq_size = 700 // self.resolution
        self.squares = [[0 for _ in range(self.resolution)] for __ in range(self.resolution)]
        self.fill = np.zeros((self.resolution, self.resolution))
        
        self.root = master
        self.canvas = Canvas(self.root, width = self.sq_size * self.resolution, height = self.sq_size * self.resolution, borderwidth = 1) # 700 = self.resolution * 25
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.canvas.bind("<Double-Button-1>", self.reset)
        self.canvas.pack()

        train = False
        test = False

        if train:
            (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
            x_train, x_test = x_train / 255.0, x_test / 255.0

            self.Model = tf.keras.models.Sequential([
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(128, activation = 'relu'),
                tf.keras.layers.Dropout(0.15),
                tf.keras.layers.Dense(10, activation = 'softmax',)
            ])

            self.Model.compile(optomizer = tf.keras.optimizers.Adam(0.001), loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'], verbose = 1)

            self.Model.fit(x_train, y_train, epochs = 10)

            self.Model.save('C:/Users/aliha/OneDrive/Desktop/model.h5py', save_format='h5')
        
        self.Model = tf.keras.models.load_model('C:/Users/aliha/OneDrive/Desktop/model.h5py')

        if test:
            (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
            x_train, x_test = x_train / 255.0, x_test / 255.0

            # print(x_train[0,:,:])

            # print(y_test)
            # print(np.argmax(self.Model.predict(x_test)))
            print(np.sum(np.argmax(self.Model.predict(x_test), 1) == y_test) / len(y_test))
            print(np.sum(np.argmax(self.Model.predict(x_train),1) == y_train) / len(y_train))

        self.reset(None)
        # self.render(self.pos)



root = Tk()
app = App(root)
root.title("Draw a number!")
root.geometry("700x700")
root.resizable(0,0)

while True:
#     # app.draw()
    root.update()
    root.update_idletasks()
root.destroy()