# Python 3 with Tkinter and Time
# -> add to vim config # nnoremap <silent> <F5> :!clear;python %<CR>

# clear for windows Note: mac is clear instead of cls
import time
import Tkinter as tk

# nul -> tuple of tuples for balanced ternary hours(3), minutes(4) and seconds(4)
def terTime():
   a = time.time() - (12*60*60) # get time with adjustment for noon = 0
   a += -5 * 60 * 60 # adjust for daylight
   a = a - (round(a / (60*60*24)) * (60*60*24)) # strip days
   h = a / (60*60) # show hours
    
   # print h # diagnostic for time adjustments
    
   lHrs = list((round(h / 9), round(((h/9) - round(h/9))*3), round(((((h/9) - round(h/9))*3) - (round(((h/9) - round(h/9))*3)))*3)))
   m = (((((h/9) - round(h/9))*3) - (round(((h/9) - round(h/9))*3)))*3) - round(((((h/9) - round(h/9))*3) - (round(((h/9) - round(h/9))*3)))*3)
   m = 60*m
   s = (m - round(m)) * 60
   lMin = list(range(4))
   lSec = list(range(4))
   c = m / 27
   d = s / 27
   for x in lMin:
      lMin[x], lSec[x] = round(c), round(d)
      c , d = (c - lMin[x])*3, (d - lSec[x])*3
   return (tuple(lHrs), tuple(lMin), tuple(lSec))

# tuple -> string
def timeString(t):
   s = "The time is "
   c = ('\x1b[1;31m@\033[0m', '\x1b[0;37m*\033[0m', '\x1b[1;34m#\033[0m')
   for i in range(3):
      s += c[int(t[0][i]+1)] + ' '
   s += 'hours;   '
   for i in range (4):
      s += c[int(t[1][i]+1)] + ' '
   s += 'minutes;   '
   for i in range (4):
      s += c[int(t[2][i]+1)] + ' '
   s += 'seconds.'
   return s



root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500, background='black')
canvas.pack()

def mkCircle(x,y, color='grey', r=20):
   """int, int [string, int] -> canvas object
      make a circle object with radius 20, centered at x, y
      with a color=grey and r = 20"""
   c = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)
   return c

L, R, G = [], [], []

# make a collection of layered circles to simulate LED.
for h in range (3):
   for v in range (4):
      if not((v==0) and (h==0)):
         for p in range(3):
            if not p:
               mkCircle(25 + p*50 + h*200, 70 + v*133) # red blue off LED
               L.append((mkCircle(25 + p*50 + h*200, 70 + v*133, 'blue'))) # blue LED
            elif p == 1:
               mkCircle(25 + p*50 + h*200, 70 + v*133) # red blue off LED
               R.append((mkCircle(25 + p*50 + h*200, 70 + v*133, 'red'))) # red LED
            else:
               mkCircle(50 + h*200, 27 + v * 133) # green off LED
               G.append(mkCircle(50 + h*200, 27 + v * 133, 'green'))
            
def showTime():
      t = tuple( i for a in terTime() for i in a)
   #if m != t:
   #   m = t
      for p,i in enumerate(t):
         canvas.itemconfig(L[p], state = 'hidden')
         canvas.itemconfig(R[p], state = 'hidden')
         canvas.itemconfig(G[p], state = 'hidden')
         if i == -1: canvas.itemconfig(L[p], state='normal')
         elif 1 == i: canvas.itemconfig(R[p], state = 'normal')
         else : canvas.itemconfig(G[p], state = 'normal')
      root.after(int(500 - (((time.time()*2) % 1) * 500)), showTime)                 

root.after(0, showTime)
root.mainloop()
