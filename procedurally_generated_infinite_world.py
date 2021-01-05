from tkinter import *
import math
import time
import random
from enum import *
from noise import _simplex

class Vector():
    x : float
    y : float
    def __init__(self, x2=0.0, y2=0.0):
        self.x = x2
        self.y = y2
    def getDirection(self):
        return (math.atan(self.y/self.x))# * 180/3.14159265358979)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __str__(self):
        return self.x, self.y
    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        else:
            return Vector(self.x * other, self.y * other)
    def getLength(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))
    def __le__(self, other):
        return (self.x <= other.x and self.y <= other.y)
    def __lt__(self, other):
        return (self.x <  other.x and self.y <  other.y)
    def __ge__(self, other):
        return (self.x >= other.x and self.y >= other.y)
    def __gt__(self, other):
        return (self.x >  other.x and self.y >  other.y)
    
    def isInBox(self, corner1, corner2):
        return (min(corner1, corner2) <= self and self <= max(corner1, corner2))

class App():
    def draw(self):
        if self.pos.isInBox(Vector(0, 0), Vector(10, 10)):
            print("In the box!")
        
    def move(self, event):
        if event.keysym == "Up":
            self.vel.y = -500
        # elif event.keysym == "Down":
        #     self.vel.y =  500
        elif event.keysym == "Right":
            self.vel.x += 30
        elif event.keysym == "Left":
            self.vel.x += -30

    def render(self, location : Vector):

        # for i in range(self.land_resolution):
        #     for j in range(self.land_resolution):
        #        self.canvas.delete(self.squares[i][j])
        
        for i in range(self.land_resolution):
            for j in range(self.land_resolution):
                x = i + location.x
                y = j + location.y
                noiseVal = _simplex.noise2(x * 0.0005 * self.land_resolution, y * self.land_resolution * 0.0005 - 5) + (y - (self.land_resolution / 2 - 5) if y < (self.land_resolution / 2 - 5) else y / 6) * 0.05
                if noiseVal > 0.0:
                    color = 'green' if (noiseVal < 0.5 and y < self.land_resolution / 2) else 'gray'
                    self.squares[i][j] = self.canvas.create_rectangle(self.size * x, self.size * y, self.size * x + self.size, self.size * y + self.size, fill = color)
        
        sq = self.squares[i][j]
        self.canvas.delete(sq)

    def __init__(self, master):
        # self.playing = Falses
        self.cur = time.time()
        
        self.pos = Vector()
        self.vel = Vector()
        self.acc = Vector()

        self.land_resolution = 100
        self.size = 800/self.land_resolution
        self.squares = [[-1] * self.land_resolution] * self.land_resolution
        
        self.canvas = Canvas(master, width = 800, height = 800, borderwidth = 0)
        self.canvas.bind("<Up>", self.move)
        self.canvas.bind("<Down>", self.move)
        self.canvas.bind("<Left>", self.move)
        self.canvas.bind("<Right>", self.move)
        self.canvas.pack()

        self.render(self.pos)



root = Tk()
app = App(root)
root.title("Infinite Procedurally Generated World")
root.geometry("800x800")
root.resizable(0,0)
while True:
    app.draw()
    root.update()
    root.update_idletasks()
root.destroy()