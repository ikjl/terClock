#!/usr/bin/env python3

import time

def clear():
   """
   none -> none 
   use ansii to clear the screen
   """
   print ('\033[2J', end="")
   return

# nul -> tuple of tuples for balanced ternary hours(3), minutes(4) and seconds(4)
def terTime(offset=.5):
   a = time.time() + offset - (12*60*60) 
   # get time with adjustment for noon = 0
   # and add offset

   a += -5 * 60 * 60 # adjust for daylight
   a = a - (round(a / (60*60*24)) * (60*60*24)) # strip days
   h = a / (60*60) # show hours
    
   # print h # diagnostic for time adjustments
    
   # unreadable code to convert to ternary...should be cleaned up.
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
def timeStringC(t):
   s = "\033[;H\n"
   c = ('\x1b[41;30m-\033[0m', '\x1b[42;30m0\033[0m', '\x1b[44;30m+\033[0m')
   for i in range (4):
      s += ' '
      for p in range (3):
         if (p==0):
            if i == 0:
               s += ' '
            else: s += c[int(t[p][i - 1]) + 1] 
         else: s += c[int(t[p][i]) + 1]
         if p != 2: s += '   '
         else: s += ' '*5 + 'times {}'.format(int(3**(3-i)))
      if i != 3: s += '\n\n'
   s += '\nhrs min sec\n\n'
   s += c[0] + ' is negative one\n'
   s += c[1] + ' is zero\n'
   s += c[2] + ' is one\033[0;0H'
   return s

def main():
   m = ""
   t = timeStringC(terTime(offset=0))
   clear()
   while True:
      if m != t:
         print(t, end="")
         m = t
      t = timeStringC(terTime())
      time.sleep(.5 - (((time.time()*2)%1)*.5))

if __name__ == '__main__': main()
