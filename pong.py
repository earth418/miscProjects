from tkinter import *
import time
import random

class App():
    def draw(self):    
        if self.playing:
            #self.cur = time.time()
            if (time.time() - self.cur) > 0.025:
                self.render()
                self.bounce()
                self.cur = time.time()
                if self.position > 720:
                    self.moy = -1
                if self.position < 80:
                    self.moy = 1
                self.position += 8 * self.moy
                self.ball[0] += 8 * self.mball[0]
                self.ball[1] += 8 * self.mball[1]
    def move(self, event):
        if event.keysym == "Up":
            self.moy = -1
        elif event.keysym == "Down":
            self.moy = 1
    def bounce(self):
        if self.ball[0] < 0: #  or self.ball[0] > 800:
            self.mball[0] *= -1
            self.velChange()
        if self.ball[0] > 800:
            self.canvas.create_text(400,400, text = "You Lose!", fill = "white", font=("", 100))
            self.playing = False
        if self.ball[1] < 0:
            self.mball[1] *= -1
            self.velChange()
        if self.ball[1] > 768:
            self.mball[1] *= -1
            self.velChange()
        if abs(self.ball[0] - 708) < 16 and abs(self.ball[1] - self.position) < 96:
            self.mball[0] *= -1
            self.score += 1
            self.velChange()
    def render(self):
        a = self.canvas.create_rectangle(776, self.position - 80, 736, self.position + 80, fill = "white")
        self.canvas.delete(self.paddle)
        self.paddle = a
        b = self.canvas.create_rectangle(self.ball[0], self.ball[1], self.ball[0] + self.size, self.ball[1] + self.size, fill = "white")
        self.canvas.delete(self.ball[2])
        self.ball[2] = b
        self.canvas.delete(self.scoreboard)
        self.scoreboard = self.canvas.create_text(85,30, text = ("Score: " + str(self.score)), font=("", 30), fill = "white")
    def velChange(self):
        self.mball[0] += (random.random()/10 - 0.05)
        self.mball[1] += (random.random()/20 - 0.025)
    def __init__(self, master):
        self.playing = True#True
        self.cur = time.time()
        self.size = 32
        self.canvas = Canvas(master, width = 800, height = 800, borderwidth = 0)
        self.canvas.bind("<Up>", self.move)
        self.canvas.bind("<Down>", self.move)
        self.ball = [400,400]
        self.canvas.pack()
        b = self.canvas.create_rectangle(self.ball[0], self.ball[1], self.ball[0] + self.size, self.ball[1] + self.size, fill = "white")
        self.ball = [400,400, b]
        r = ((random.random() + 5) / 6) * 2 - 1
        self.mball = [r, pow(1 - pow(r, 2), 0.5) * r/abs(r)]
        self.canvas.focus_set()
        self.position = 400
        a = self.canvas.create_rectangle(776, self.position, 736, self.position + 160, fill = "white")
        c = self.canvas.create_text(15, 15, fill = "white", text = "Score: 0", font=("", 30))
        self.scoreboard = c
        self.paddle = a
#        for x in range(26):
#            for y in range(26):
        self.canvas.create_rectangle(0,0,800,800, fill = "black")#, self.size * y, self.size * x + self.size, self.size * y + self.size, fill = "black")
        self.moy = 0
        self.score = 0

root = Tk()
app = App(root)
root.title("Pong")
root.geometry("800x800")
root.resizable(0,0)
while True:
    app.draw()
    root.update()
    root.update_idletasks()
root.destroy()