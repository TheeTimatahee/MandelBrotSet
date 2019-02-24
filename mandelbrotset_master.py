####!/usr/bin/env python 1
from tkinter import *
from datetime import date, time, datetime
from PIL import ImageTk, Image
import numpy as np
import math
import calendar
import time

class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Mandelbrot Set")
        width = 900; height = 900
        self.root.geometry(str(width) + "x" + str(height))
        self.root.config(background='grey')

        # self.img = ImageTk.PhotoImage(Image.open("atprstd.png"))
        self.panel = Label(self.root)
        # self.panel.pack(side = "bottom", fill = "both", expand = "yes")

        # frame = Frame(master=self.root, width=500, height=500)
        # frame.pack()

        menu = Menu(self.root)
        self.root.config(menu=menu)

        programsMenu = Menu(menu)
        menu.add_cascade(label="Programs", menu=programsMenu)
        i = mandelbrot(width,height,d=2)
        programsMenu.add_command(label="Mandelbrot, d=2", command=self.displayImage(i))
        #programsMenu.add_command(label="yeet", command=self.displayImage('atprstd.png'))

        optionsMenu = Menu(menu)
        menu.add_cascade(label="Options", menu=optionsMenu)
        #optionsMenu.add_command(label="Save Image...", command=Mandelbrot.saveImage(self.img))
        optionsMenu.add_command(label="Clear Screen...", command=self.clear)

        self.root.mainloop()

    @staticmethod
    def saveImage(img,location="C:\\"):
        PhotoImage.write(img,filename="mandelbrot", format=".png", from_coords=location)

    def displayImage(self,image):
        self.panel.destroy()
        self.img = ImageTk.PhotoImage(Image.open(image))
        self.panel = Label(self.root, image = self.img)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")

    def clear(self):
        print("beep")

def mandelbrot(width, height, d=2, zoom=1):
    """Returns the image of the Mandelbrot set given 'd'
    as a .png"""
    print("Performing preparations...")
    startTime = float(time.time())
    bitMapArray = np.zeros([height, width, 3], dtype=np.uint8)
    print("Calculating Mandelbrot Set...")
    for x in range(0,width):
        for y in range(0,height):
            coords = screenToCartesian(x,y,width,height,zoom)
            if(coords[0] == 0):
                zeroX = x
            if(coords[1] == 0):
                zeroY = y
            n = testCoord(coords[0],coords[1],d)
            color(bitMapArray,x,y,n,255//3,255//3)
    bitMapArray = mapAxis(bitMapArray,width,height,zeroX,zeroY)
    img = Image.fromarray(bitMapArray)
    name = "mandelbrot-" + currentTime() + ".png"
    img.save(name)
    #name = 'atprstd.png'
    timeTaken = (float(time.time())) - startTime
    print("Done - Saved as: " + name)
    print("Time taken to output: " + str(timeTaken) + " seconds")
    return name

def color(bitMapArray,x,y,r,g,b):
    bitMapArray[y][x] = [r,g,b]
    return bitMapArray

def mapAxis(bitMapArray,width,height,zeroX=-1,zeroY=-1):
    """Maps axis onto a give bitmap in the form of
       black pixels"""
    if(zeroX == -1 or zeroY == -1):
        for x in range(0,width):
            for y in range(0,height):
                coords = screenToCartesian(x,y,width,height)
                if(coords[0] == 0):
                    zeroX = x
                if(coords[1] == 0):
                    zeroY = y
    for y in range(0,height):
        bitMapArray[y][zeroX] = [0,0,0]
    for x in range(0,width):
        bitMapArray[zeroY][x] = [0,0,0]
    return bitMapArray

def screenToCartesian(x,y,width=500,height=500,zoom=1):
    """Converts coords corresponding to a pixel on the screen
    to coords on the complex plane"""
    scale = ((2.5*zoom)/(width/2))
    cartX = (x - width/2.0)*scale
    cartY = (height/2.0 - y)*scale
    return [cartX,cartY]

def currentTime():
    return str(date.today().month) + "-" + str(date.today().day) + "-" + str(date.today().year) + "-" + str(datetime.now().hour) + ";" + str(datetime.now().minute) + ";" + str(datetime.now().second)

def cartesianToScreen(x,y,zoom=1):
    pass

def testCoord(x,y,d):
    """Determines whether or not the given complex point is
    a part of the Mandelbrot Set with given 'd'"""
    n = 0
    maxN = 32
    z = complex(0,0)
    coord = complex(x,y)
    while(n < maxN and complexAbs(z) <= 100):
        z = z**d + coord
        n += 1
    return math.ceil(n*(3.984375*2))

def complexAbs(z):
    """Calculates the absolute value of complex number
    'z' for use in 'testCoord'"""
    return math.sqrt((z.real**2)+(z.imag**2))

side = 4000
# m = App()
mandelbrot(side,side)
# a = screenToCartesian(125,250)
# print("x = " + str(a[0]) + ", y = " + str(a[1]))