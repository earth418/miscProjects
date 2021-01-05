from tkinter import *
import math
import time
import random

def sign(x):
    if x is 0:
        return 0
    elif x > 0:
        return 1
    else: return -1

class Vector():
    x : float
    y : float
    def __init__(self, x2, y2=None):
        if y2 is None:
            self.x = math.cos(x2)
            self.y = math.sin(x2)
        else:
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
    

class App():
    def draw(self):
        if self.playing:
            # onRamp = True
            if (time.time() - self.cur) > 0.01:
                if self.pos.x > 600 and self.pos.y > 500 - (self.pos.x - 800) / 2:
                    # self.vel *= math.cos(3.14159265358979 + self.iangle)# * -0.5)
                    # onRamp = True
                    self.acc += Vector(self.iangle) * -9.81
                    self.acc += Vector(self.iangle) * sign(self.acc.x) * 9.81
                    self.pos.y = 500 - (self.pos.x - 800) / 2
                else:
                    # if onRamp:
                    # self.vel.y = 0
                        # onRamp = False
                    self.acc = Vector(0, 981)
                if self.pos.y > 600 and self.vel.y > 0:
                    self.vel.y *= -0.5
                    self.pos.y = 600
                    # onRamp = False
                elif self.pos.y <= 600:
                    self.acc.y = 981
                    # onRamp = False
                self.render()
                self.vel += self.acc * 0.01
                self.pos += self.vel * 0.01
                if self.pos.y >= 600:
                    self.acc.x -= self.mass * 0.1 * sign(self.acc.x)
                    self.vel.x -= (time.time() - self.cur) * 500 * sign(self.vel.x)
                # self.acc.x = 0
                self.cur = time.time()
    def move(self, event):
        if event.keysym == "Up":
            self.vel.y = -500
        elif event.keysym == "Down":
            self.vel.y =  500
        elif event.keysym == "Right":
            self.vel.x += 30
        elif event.keysym == "Left":
            self.vel.x += -30
        if self.playing is False:
            self.acc.x = 0
            self.vel.x = 0
            self.playing = True
    def render(self):
        self.canvas.delete(self.char)
        self.char = self.canvas.create_oval(self.pos.x, self.pos.y, self.pos.x + 30, self.pos.y + 30, fill = "black")
        self.canvas.delete(self.a)
        self.canvas.delete(self.b)
        self.canvas.delete(self.c)
        self.a = self.canvas.create_line(200, 400, 200 + (self.pos.x - 400) / 10, 400 + (self.pos.y - 600) / 10)
        self.b = self.canvas.create_line(400, 400, 400 + self.vel.x / 10, 400 + self.vel.y / 10)
        self.c = self.canvas.create_line(600, 400, 600 + self.acc.x / 10, 400 + self.acc.y / 10)
    def __init__(self, master):
        self.playing = False#True
        self.cur = time.time()
        self.size = 30
        self.canvas = Canvas(master, width = 800, height = 800, borderwidth = 0)
        self.canvas.bind("<Up>", self.move)
        self.canvas.bind("<Down>", self.move)
        self.canvas.bind("<Left>", self.move)
        self.canvas.bind("<Right>", self.move)
        self.canvas.pack()
        self.canvas.focus_set()
        self.char = self.a = self.b = self.c = 0
        self.canvas.create_rectangle(0, 800, 800, 630, fill="green")
        self.canvas.create_polygon(600, 630, 800, 630, 800, 530)
        self.iangle = math.atan((630-530)/(600-800))
        self.mass = 10
        self.coefffrict = 0.5
        self.acc = Vector(0,981) #10 cubes per meter
        self.vel = Vector(0,0)
        self.pos = Vector(400,600)

root = Tk()
app = App(root)
root.title("Physics Game")
root.geometry("800x800")
# root.resizable(0,0)
while True:
    app.draw()
    root.update()
    root.update_idletasks()
root.destroy()