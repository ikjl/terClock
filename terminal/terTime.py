# nnoremap <silent> <F5> :!clear;python %<CR>

# clear for windows Note: mac is clear instead of cls

import os
def clear():
   os.system('clear')

import time

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

def main():
   m = ""
   while True:
      t = timeString(terTime())
      if m != t:
         m = t
         clear()
         print(t)
      time.sleep(.5 - (((time.time()*2)%1)*.5))

if __name__ == '__main__': main()
