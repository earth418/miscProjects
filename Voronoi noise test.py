from math import *
from random import *
from tkinter import *

class Vec2:

    def __init__(self, x, y):
        self.X = x
        self.Y = y
    
    def __mul__(self, value):
        if isinstance(value, Vec2):
            return Vec2(self.X * value.X, self.Y * value.Y)
        else:
            return Vec2(value * self.X, value * self.Y)
    
    def __add__(self, value):
        if isinstance(value, Vec2):
            return Vec2(self.X + value.X, self.Y + value.Y)
        else:
            return Vec2(value + self.X, value + self.Y)
    
    def __sub__(self, value):
        return Vec2(self.X - value.X, self.Y - value.Y)

    def len(self):
        return sqrt(self.dot(self))

    def __str__(self):
        return f'({self.X}, {self.Y})'

    def dot(self, other):
        return self.X * other.X + self.Y * other.Y
    
    def sin(self):
        return Vec2(sin(self.X), sin(self.Y))
    
    def floor(self):
        return Vec2(floor(self.X), floor(self.Y))


# points = [Vec2(j + random() - 0.5, k + random() - 0.5) for j in [-1, 0, 1] for k in [-1, 0, 1]]

def rand2dTo1d(value : Vec2, dotDir = Vec2(12.9898, 78.233)):
    smallValue = value.sin()
    random = smallValue.dot(dotDir)
    random = sin(random) * 143758.5453
    return (random - floor(random))

def rand2dTo2d(value : Vec2):
    return Vec2(   
        rand2dTo1d(value, Vec2(12.989, 78.233)),
        rand2dTo1d(value, Vec2(39.346, 11.135))
    )
    

def Voronoi(In : Vec2):

    bcell = In.floor()

    min_dist = 50
    closest_pt = Vec2(0, 0)

    pts = []
    for j in [-1, 0, 1]:
        for k in [-1, 0, 1]:
            cell = bcell + Vec2(j, k)
            pts.append(cell + rand2dTo2d(cell))

    for pnt in pts:
        dist = (In - pnt).len()
        if dist <= min_dist:
            min_dist = dist
            closest_pt = pnt

    # for pt in pts:
    #     dc = (In - pt).len()
    #     dx = abs(In.X - pt.X)
    #     if dc < min_dist:
    #         min_dist = dc
    #         closest_pt = pt
    #     if dx > min_dist:
    #         break

    min_dist = min(min_dist, 1.0)

    return min_dist, closest_pt
    
def fBm_Voronoi(In : Vec2, persistence : float, lacunarity : float, octaves : int):
    pers = 1
    lac = 1
    noise = 0
    for _ in range(octaves):
        noise += pers * Voronoi(In * lac)[0]
        lac *= lacunarity
        pers *= persistence
    return noise * persistence

def color(c):
    v = hex(c)[2:]
    if len(v) == 1:
        v = '0' + v
    return '#' + v * 3

class App:
    def __init__(self, master=None):
        self.root = master
        self.canvas = Canvas(background='#FFFFFF', height=5500, width=500)
        self.canvas.pack()

    def update(self, loc):
        size = 10
        for i in range(0, 500, size):
            for j in range(0, 500, size):
                u = i / 100
                v = j / 100
                # Vor, p = Voronoi(Vec2(u, v))
                Vor = fBm_Voronoi(Vec2(u, v) + loc, 0.5, 2, 1)
                c = color(floor(255 * Vor))
                # CellColor = '#' + hex(int(255 * 255 * 255 * rand2dTo1d(p)))[2:]
                # while len(CellColor) != 7:
                #     CellColor += '0'

                self.canvas.create_rectangle(i, j, i + size, j + size, fill=c)
                # self.canvas.create_rectangle(i, j, i + 15, j + 15, fill=lColor.toHex())


root = Tk()
app = App(root)

# app.update()

# someloc = Vec2(0.0, 0.0)
see = 0

root.geometry('500x500')
while True:
    app.update(see)
    root.update()

    see += 0.5
    # someloc.Y -= 0.2
# root.mainloop()
