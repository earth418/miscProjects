from tkinter import *
import math
import time
import random

class App():
    def draw(self):
        self.boolean = False
        speed = 25
        for piece in self.movingpieces:
            self.canvas.move(piece[0], piece[2]/speed, piece[3]/speed)
            piece[1] += 1
            if piece[1] >= speed:
                self.movingpieces.remove(piece)
    def interp(self, piece, directionx, directiony):
        self.movingpieces.append([piece,0,directionx,directiony])
    def isMovesLeft(self):
        for a in [0,4,8,12]:
            print(self.pieces[a], self.pieces[a + 1], self.pieces[a + 2], self.pieces[a + 3])
        print("----------------------------------------------------------")
        if (self.pieces.count([0,0,0]) >= 1):
            return True
        for x in range(16):
            n = self.pieces[x][0]
            if (x < 15 == self.pieces[x + 1][0] and (x+1) % 4 != 0):
                print("found +1")
                return True
            if (x > 0 and n == self.pieces[x - 1][0] and (x+1) % 4 != 1):
                print("found -1")
                return True
            if (x < 12 and n == self.pieces[x + 4][0]):
                print('found +4')
                return True
            if (x > 3 and n == self.pieces[x - 4][0]):
                print('found -4')
                return True
        return False
    def postMove(self):
        if not(self.isMovesLeft()):
            self.canvas.create_text(400,400, text = "You Lose!", font=("", 100))
    def updateColor(self, curPos):
        val = self.pieces[curPos][0]
        if val > 0:
            b = int(math.log2(val))
            color = [210 - 17 * b,180 - 15 * b,140 - 12 * b]
            st = "#"
            for m in color:
                st += hex(m).split('x')[-1]
            self.canvas.itemconfig(self.pieces[curPos][1], fill = st)
    def move(self, event):
        movement = 0
        mx = 0
        my = 0
        somethingMoved = False
        if event.keysym == "Up":
            movement = - 4
            mx = 0
            my = -1
        elif event.keysym == "Down":
            movement = 4
            mx = 0
            my = 1
        elif event.keysym == "Right":
            movement = 1
            mx = 1
            my = 0
        elif event.keysym == "Left":
            movement = -1
            mx = -1
            my = 0
        mx *= self.size
        my *= self.size
        for x in range(len(self.pieces)):
            curPos = x
            while (True):
                if self.pieces[curPos][0] >= 0:
                    try:
                        if self.pieces[curPos + movement][0] == 0:
                            self.interp(self.pieces[curPos][1], mx, my)
                            self.interp(self.pieces[curPos][2], mx, my)
                            #self.canvas.move(self.pieces[curPos][1], 0, my)
                            #self.canvas.move(self.pieces[curPos][2], 0, my)
                            self.pieces[curPos + movement] = self.pieces[curPos][:]
                            self.pieces[curPos] = [0,0,0]
                            curPos += movement
                            somethingMoved = True
                        elif self.pieces[curPos + movement][0] == self.pieces[curPos][0]:
                            self.interp(self.pieces[curPos][1], mx, my)
                            self.interp(self.pieces[curPos][2], mx, my)
                            self.canvas.delete(self.pieces[curPos][1])
                            self.canvas.delete(self.pieces[curPos][2])
                            self.canvas.itemconfig(self.pieces[curPos + movement][2], text = self.pieces[curPos + movement][0] * 2)
                            self.pieces[curPos] = [0,0,0]
                            self.pieces[curPos + movement][0] *= 2
                            self.updateColor(curPos + movement)
                            somethingMoved = True
                            break
                        else:
                            break
                    except:
                        break
                else:
                    break
            self.updateColor(curPos)
        if somethingMoved:
            self.createSquare()
        self.postMove()
    def arrowUp(self, event):
        somethingMoved = False
        for x in range(len(self.pieces)):
            curPos = x
            while (True):
                if self.pieces[curPos][0] > 0 and curPos - 4 >= 0:
                    if self.pieces[curPos - 4][0] == 0:
                        self.interp(self.pieces[curPos][1], 0, -1 * self.size)
                        self.interp(self.pieces[curPos][2], 0, -1 * self.size)
                        #self.canvas.move(self.pieces[curPos][1], 0, -1 * self.size)
                        #self.canvas.move(self.pieces[curPos][2], 0, -1 * self.size)
                        self.pieces[curPos - 4] = self.pieces[curPos][:]
                        self.pieces[curPos] = [0,0,0]
                        curPos -= 4
                        somethingMoved = True
                    elif self.pieces[curPos - 4][0] == self.pieces[curPos][0]:
                        self.interp(self.pieces[curPos][1], 0, -1 * self.size)
                        self.interp(self.pieces[curPos][2], 0, -1 * self.size)
                        self.canvas.delete(self.pieces[curPos][1])
                        self.canvas.delete(self.pieces[curPos][2])
                        self.canvas.itemconfig(self.pieces[curPos - 4][2], text = self.pieces[curPos - 4][0] * 2)
                        self.pieces[curPos] = [0,0,0]
                        self.pieces[curPos - 4][0] *= 2
                        self.updateColor(curPos - 4)
                        somethingMoved = True
                        break
                    else:
                        break
                else:
                    break
            self.updateColor(curPos)
        if somethingMoved:
            self.createSquare()
        self.postMove()
        print(len(self.pieces))
    def arrowDown(self, event):
        somethingMoved = False
        for x in range(len(self.pieces)):
            curPos = x
            while (True):
                if self.pieces[curPos][0] > 0 and curPos + 4 < 16:
                    if self.pieces[curPos + 4][0] == 0:
                        #self.canvas.move(self.pieces[curPos][1], 0, self.size)
                        #self.canvas.move(self.pieces[curPos][2], 0, self.size)
                        self.interp(self.pieces[curPos][1], 0, self.size)
                        self.interp(self.pieces[curPos][2], 0, self.size)
                        self.pieces[curPos + 4] = self.pieces[curPos][:]
                        self.pieces[curPos] = [0,0,0]
                        curPos += 4
                        somethingMoved = True
                    elif self.pieces[curPos + 4][0] == self.pieces[curPos][0]:
                        self.interp(self.pieces[curPos][1], 0, self.size)
                        self.interp(self.pieces[curPos][2], 0, self.size)
                        time.sleep(0.05)
                        self.canvas.delete(self.pieces[curPos][1])
                        self.canvas.delete(self.pieces[curPos][2])
                        self.canvas.itemconfig(self.pieces[curPos + 4][2], text = self.pieces[curPos + 4][0] * 2)
                        self.pieces[curPos] = [0,0,0]
                        self.pieces[curPos + 4][0] *= 2
                        self.updateColor(curPos + 4)
                        somethingMoved = True
                        break
                    else:
                        break
                else:
                    break
            self.updateColor(curPos)
        if somethingMoved:
            self.createSquare()
        self.postMove()
    def arrowLeft(self, event):
        somethingMoved = False
        for x in range(len(self.pieces)):
            curPos = x
            while (True):
                if self.pieces[curPos][0] > 0 and curPos % 4 - 1 >= 0:
                    if self.pieces[curPos - 1][0] == 0:
                        #self.canvas.move(self.pieces[curPos][1], -1 * self.size, 0)
                        #self.canvas.move(self.pieces[curPos][2], -1 * self.size, 0)
                        self.interp(self.pieces[curPos][1], -1 * self.size, 0)
                        self.interp(self.pieces[curPos][2], -1 * self.size, 0)
                        self.pieces[curPos - 1] = self.pieces[curPos][:]
                        self.pieces[curPos] = [0,0,0]
                        somethingMoved = True
                        curPos -= 1
                    elif self.pieces[curPos - 1][0] == self.pieces[curPos][0]:
                        self.canvas.delete(self.pieces[curPos][1])
                        self.canvas.delete(self.pieces[curPos][2])
                        self.canvas.itemconfig(self.pieces[curPos - 1][2], text = self.pieces[curPos - 1][0] * 2)
                        self.pieces[curPos] = [0,0,0]
                        self.pieces[curPos - 1][0] *= 2
                        self.updateColor(curPos - 1)
                        somethingMoved = True
                        break
                    else:
                        break
                else:
                    break
            self.updateColor(curPos)                    
        if somethingMoved:
            self.createSquare()
        self.postMove()
    def arrowRight(self, event):
        somethingMoved = False
        for x in range(len(self.pieces)):
            curPos = x
            while (True):
                if self.pieces[curPos][0] > 0 and curPos % 4 + 1 < 4:
                    if self.pieces[curPos + 1][0] == 0:
                        #self.canvas.move(self.pieces[curPos][1], self.size, 0)
                        #self.canvas.move(self.pieces[curPos][2], self.size, 0)
                        self.interp(self.pieces[curPos][1], self.size, 0)
                        self.interp(self.pieces[curPos][2], self.size, 0)
                        self.pieces[curPos + 1] = self.pieces[curPos][:]
                        self.pieces[curPos] = [0,0,0]
                        curPos += 1
                        somethingMoved = True
                    elif self.pieces[curPos + 1][0] == self.pieces[curPos][0]:
                        self.canvas.delete(self.pieces[curPos][1])
                        self.canvas.delete(self.pieces[curPos][2])
                        self.canvas.itemconfig(self.pieces[curPos + 1][2], text = self.pieces[curPos + 1][0] * 2)
                        self.pieces[curPos] = [0,0,0]
                        self.pieces[curPos + 1][0] *= 2
                        self.updateColor(curPos + 1)
                        somethingMoved = True
                        break
                    else:
                        break
                else:
                    break
            self.updateColor(curPos)
        if somethingMoved:
            self.createSquare()
        self.postMove()
    def createSquare(self):
        val = random.randint(1,2) * 2
        while(True):
            posx = random.randint(0,3)
            posy = random.randint(0,3)
            if self.pieces[(posy * 4 + posx)][0] == 0:
                break
            else:
                continue
        b = self.canvas.create_rectangle(posx * self.size, posy * self.size, posx * self.size + self.size, self.size*(posy + 1), fill = "tan")
        c = self.canvas.create_text(posx * self.size + self.size/2, posy*self.size + self.size/2, text = val, font = ("",80))
        #self.creating = b
        self.pieces[posx + posy * 4] = [val, b, c]
        self.updateColor(posx + posy * 4)
    def __init__(self, master):
        self.size = 200
        self.movingpieces = []
        self.creating = -1
        self.canvas = Canvas(master, width = 800, height = 800, borderwidth = 12)
        self.canvas.bind("<Up>", self.arrowUp)
        self.canvas.bind("<Down>", self.arrowDown)
        self.canvas.bind("<Left>", self.arrowLeft)
        self.canvas.bind("<Right>", self.arrowRight)
        self.canvas.pack()
        self.canvas.focus_set()
        for x in range(4):
            for y in range(4):
                self.canvas.create_rectangle(self.size * x, self.size * y, self.size * x + self.size, self.size * y + self.size)
        self.pieces = []
        for m in range(16):
            self.pieces.append([0,0,0])
        print(self.pieces)
        self.createSquare()
        self.createSquare()

root = Tk()
app = App(root)
root.title("2048")
root.geometry("812x812")
root.resizable(0,0)
while True:
    app.draw()
    root.update()
    root.update_idletasks()
root.destroy()