from tkinter import *
import math
import time
import random
from enum import *

    
class App():
    def draw(self):
        if self.playing:
            if (time.time() - self.cur) > 0.1:
                self.mx = self.mox
                self.my = self.moy
                self.render()
                self.cur = time.time()
                self.position[0] += 32 * self.mx
                self.position[1] += 32 * self.my
            if abs(self.position[0] - self.apple[0]) < 16 and abs(self.position[1] - self.apple[1]) < 16:
                self.snakeLength += 1
                self.canvas.delete(self.apple[2])
                self.addFruit()
            if self.position[0] < -16 or self.position[0] > (784+16) or self.position[1] < -16 or self.position[1] > (784 + 16):
                self.canvas.create_text(400,400, text = "You Lose!", fill = "white", font=("", 100))
                self.playing = False    
            for pos in self.snake[1:]:
                if pos[0] == self.position[0] and pos[1] == self.position[1]:
                    self.canvas.create_text(400,400, text = "You Lose!", fill = "white", font=("", 100))
                    self.playing = False
    def move(self, event):
        if event.keysym == "Up" and self.my != 1:
            self.mox = 0
            self.moy = -1
        elif event.keysym == "Down" and self.my != -1:
            self.mox = 0
            self.moy = 1
        elif event.keysym == "Right" and self.mx != -1:
            self.mox = 1
            self.moy = 0
        elif event.keysym == "Left" and self.mx != 1:
            self.mox = -1
            self.moy = 0
        self.playing = True
    def addFruit(self):
        locx = random.randint(1,24) * 32
        locy = random.randint(1,24) * 32
        aid = self.canvas.create_rectangle(locx, locy, locx + 32, locy + 32, fill = "red")
        self.apple = [locx, locy, aid]
    def render(self):
        a = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + 32, self.position[1] + 32, fill = "green")
        self.snake.append([self.position[0], self.position[1], a])
        if len(self.snake) > self.snakeLength:
            self.canvas.delete(self.snake[0][2])#self.snake[len(self.snake) - 1][2])
            self.snake.remove(self.snake[0])#self.snake[len(self.snake) - 1])
    def __init__(self, master):
        self.playing = False#True
        self.cur = time.time()
        self.size = 32
        self.canvas = Canvas(master, width = 800, height = 800, borderwidth = 0)
        self.canvas.bind("<Up>", self.move)
        self.canvas.bind("<Down>", self.move)
        self.canvas.bind("<Left>", self.move)
        self.canvas.bind("<Right>", self.move)
        self.canvas.pack()
        self.canvas.focus_set()
        self.position = [416,416]
        a = self.canvas.create_rectangle(self.position[0], self.position[1], self.position[0] + 32, self.position[1] + 32, fill = "green")
        self.snake = [[416,416, a]]
        self.apple = [400,600]
        for x in range(26):
            for y in range(26):
                self.canvas.create_rectangle(self.size * x, self.size * y, self.size * x + self.size, self.size * y + self.size, fill = "black")
        self.addFruit()
        self.snakeLength = 1
        self.mox = self.moy = 0
        self.mx = self.my = 0
        #self.my = -1

root = Tk()
app = App(root)
root.title("Snake")
root.geometry("800x800")
root.resizable(0,0)
while True:
    app.draw()
    root.update()
    root.update_idletasks()
root.destroy()