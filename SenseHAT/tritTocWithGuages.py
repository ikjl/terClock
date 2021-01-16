#!/usr/bin/env python3
from sense_hat import SenseHat
from sense_emu import SenseHat as SHE
sEmu = SHE()
sense = SenseHat()
from math import log, atan, pi
from datetime import datetime, timedelta
from time import sleep

# clear disply
sense.clear()

# set estheticly pleasing (not to bright) gamma
# a compramise between dimness and contrast
sense.gamma = (0, 1, 1, 1, 1, 2, 2, 2,
               3, 3, 3, 4, 4, 4, 5, 5,
               6, 6, 7, 7, 8, 8, 9, 9,
               10, 10, 11, 12, 13, 14, 15, 17)

# make emu match aesthetics of adjustied sense hat
sEmu.gamma = (0, 1, 2, 4, 8, 16, 31, 31, 
              31, 31, 31, 31, 31, 31, 31, 31, 
              31, 31, 31, 31, 31, 31, 31, 31, 
              31, 31, 31, 31, 31, 31, 31, 31, 
              )

# tuple of default trit colors. A four touple of touples with 3 iintegers representing colors
# for -1, 0, 1 and trimal point.
dTritColors = ((64, 0, 0), (0, 0, 0), (64, 16, 0), (0, 16, 0))

# requires "from math import log"
# convert to balanced ternary
# anInt -> aTuple of -1, 0, 1
def toTer(anInt):
    if abs(anInt) < .5: return tuple((0,))
    outList = []
    sizeInt = int(log(2*abs(anInt), 3))
    for i in range(sizeInt+1):
        outList.append( -1 if anInt % 3 > 1.5 else int(anInt % 3))
        anInt = (anInt - outList[i])/3
    return tuple(outList)

# test of toTer()
toTerTestBol = [toTer(i) for i in range(-14, 15, 1)] == [(1, 1, 1, -1), (-1, -1, -1), (0, -1, -1), (1, -1, -1), (-1, 0, -1), (0, 0, -1), (1, 0, -1), (-1, 1, -1), (0, 1, -1), (1, 1, -1), (-1, -1), (0, -1), (1, -1), (-1,), (0,), (1,), (-1, 1), (0, 1), (1, 1), (-1, -1, 1), (0, -1, 1), (1, -1, 1), (-1, 0, 1), (0, 0, 1), (1, 0, 1), (-1, 1, 1), (0, 1, 1), (1, 1, 1), (-1, -1, -1, 1)]
print ("toTer() passed -14 to 14 test:{}".format(toTerTestBol))

# some lines used in testing code and creating testing routine
# print(toTer(-11))
# print([toTer(i) for i in range(-14, 15, 1)])

# touple of trits (-1, 0, 1), trimal places integer, rowInt, tuple of four (r, g, b) colors
# -> none (displays a row on the sense at LED matrix
def showTerneryRow(tritTuple, trimalInt=0, rowInt=7, tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 48, 0))):
   for x in range(8):          
      if x < len(tritTuple) and (x < trimalInt or trimalInt ==0):
         sense.set_pixel(7 - x, rowInt, tritColors[tritTuple[x]+1])
      # add tritsmel place
      elif x == trimalInt != 0 : sense.set_pixel(7-x, rowInt, tritColors[3])
      elif 0 != trimalInt < x < len(tritTuple) + 1:
         sense.set_pixel(7 - x, rowInt, tritColors[tritTuple[x-1]+1])
      else: sense.set_pixel (7 - x, rowInt, (0, 0, 0))

# requires from math import atan, pi, round
# tupleOfColros, rowInt
# , rFloat to adjust roation in 8ths of a circle counter clockwise
# , flipBol to reverse x directio which correct for upside down hat.
# -> none
# display magnitomiter in ternary in a circle that indicates direction.
# starting at top and going clockwise.
def showMag(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 8, 0)), rFloat = -2.5, flipBol = True):
   squareTuple = ((1, 0), (0, 0), (0,1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0))
   magTuple = tuple(sense.get_compass_raw().values())
   if flipBol: magTuple = magTuple[0]*-1, magTuple[1], magTuple[2]
   # find magnitude
   magInt = sum(i**2 for i in magTuple)**.5
   magTritTuple = toTer(magInt)
   # handle the case of cosine = 0, and make positive by adding pi / 4
   if magTuple[0] == 0: directionFloat = pi/2 if magTuple[1] > 0 else 0
   else: directionFloat = atan(magTuple[1]/magTuple[0] + (pi*3/4 if magTuple[0] < 0 else pi/4) )
   # scale direction to 8 positions
   directionFloat = (directionFloat*8/pi + rFloat) % 8
   print (directionFloat)
   # find the position of the left (couter clockwise) and right pixels
   diffFloat = directionFloat - int(directionFloat)
   leftInt = (int(directionFloat) + (1 if diffFloat == 0 else 0)) % 8
   rightInt = (leftInt - 1) % 8
   maxBrightInt = 127
   leftBrightInt = round(maxBrightInt if diffFloat == 0 else maxBrightInt * diffFloat, 0)
   rightBrightInt = maxBrightInt - leftBrightInt
   leftColorTuple = tuple(int(round(leftBrightInt*i/max(tritColors[3]),0)) for i in (tritColors[3]))
   rightColorTuple = tuple(int(round(rightBrightInt*i/max(tritColors[3]),0)) for i in (tritColors[3]))
   #print(('leftInt:',leftInt, 'rightInt:', rightInt, 'diff', diffFloat))
   #print(('left', leftColorTuple, 'right', rightColorTuple))
   for i in range (8):
      if i == 0: sense.set_pixel(squareTuple[leftInt][0], squareTuple[leftInt][1], leftColorTuple)
      elif i == 7: sense.set_pixel(squareTuple[rightInt][0], squareTuple[rightInt][1], rightColorTuple)
      elif i <= len(magTritTuple):
         sense.set_pixel(squareTuple[(leftInt + i) % 8][0], squareTuple[(leftInt + i) % 8][1], tritColors[magTritTuple[i-1]+1])
      else: sense.set_pixel(squareTuple[(leftInt + i) % 8][0], squareTuple[(leftInt + i) % 8][1], (0, 0, 0))
   
   
   
# tupleOfColros, rowInt -> none
# display humidity in ternary on the rowInt + 1 row of the sense led display
def showHumidity(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 48, 0)), rowInt=4):
   hTuple = toTer(round(sense.get_humidity()*3, 0))
   for x in range(8):
      if x < len(hTuple) and x < 1: sense.set_pixel(7 - x, rowInt, tritColors[hTuple[x]+1])
      # add tritsmel place
      elif x == 1: sense.set_pixel(7-x, rowInt, tritColors[3])
      elif 1 < x < len(hTuple) + 1: sense.set_pixel(7 - x, rowInt, tritColors[hTuple[x-1]+1])
      else: sense.set_pixel (7 - x, rowInt, (0, 0, 0))

# tupleOfColros, rowInt -> none
# display pressure in ternary on the rowInt + 1 row of the sense led display
def showPressure(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0)), rowInt=3):
   pTuple = toTer(round(sense.get_pressure(), 0))
   for x in range(8):
      if x < len(pTuple):
         sense.set_pixel(7 - x, rowInt, tritColors[pTuple[x]+1])
      else: sense.set_pixel (7 - x, rowInt, (0, 0, 0))

# requires from math import log
# tupleOfColros, rowInt -> none
# display temperature in kjeils formated to ternary on the rowInt +1th row of the sense led display
# kjeils are a lograthmic temperature scale with zero at 300 K and -1000 at 1K
# Show one tritismel place
def showKjeils(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 48, 0)), rowInt=5):
   # convert to Kelvin
   kelvinFloat = sense.get_temperature() + 273.15
   # convert to kjeils
   kjeilFloat = log(kelvinFloat/300, 300**(1/1000))
   # multiply by 9 to add two tritismel places
   kjeilInt = round(kjeilFloat*9,0)
   #print(kjeilInt)
   kTuple = toTer(kjeilInt)
   for x in range(8):
      if x < len(kTuple) and x < 2: sense.set_pixel(7 - x, rowInt, tritColors[kTuple[x]+1])
      # add tritsmel place
      elif x == 2: sense.set_pixel(7-x, rowInt, tritColors[3])
      elif 2 < x < len(kTuple) + 1: sense.set_pixel(7 - x, rowInt, tritColors[kTuple[x-1]+1])
      else: sense.set_pixel (7 - x, rowInt, (0, 0, 0))

# requires from math import log
# tupleOfColros rowInt -> none
# display temperature in exKelvins or exponential kelvins where 0 exK = 1 Kelvin
# and 1 exK = 10 Kelvin. 10^(temp in exK)  = temp in K
# Show one tritismel place
def showExK(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 48, 0)), rowInt=7):
   # convert to Kelvin
   kelvinFloat = sense.get_temperature() + 273.15
   # convert to kjeils
   exKFloat = log(kelvinFloat, 10)
   # multiply by 3**trimalInt to add trimalInt trimal places
   trimalInt = 5
   exKInt = round(exKFloat*3**trimalInt,0)
   #print(exKInt)
   kTuple = toTer(exKInt)
   for x in range(8):
      if x < len(kTuple) and x < trimalInt: sense.set_pixel(7 - x, rowInt, tritColors[kTuple[x]+1])
      # add tritsmel place
      elif x == trimalInt: sense.set_pixel(7-x, rowInt, tritColors[3])
      elif trimalInt < x < len(kTuple) + 1: sense.set_pixel(7 - x, rowInt, tritColors[kTuple[x-1]+1])
      else: sense.set_pixel (7 - x, rowInt, (0, 0, 0))

# tupleOfColros rowInt -> none
# display temperature in celcius
def showCelcius(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 48, 0)), rowInt=6):
   # multiply by 3**trimalInt to add trimalInt trimal places
   trimalInt = 1
   celciusInt = round(sense.get_temperature()*3**trimalInt,0)
   cTuple = toTer(celciusInt)
   showTerneryRow(cTuple, trimalInt, rowInt, tritColors)

# tupleOfColros rowInt -> none
# display temperature in Fahrenheit
def showFahrenheit(tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0), (0, 48, 0)), rowInt=7):
   # multiply by 3**trimalInt to add trimalInt trimal places
   trimalInt = 0
   fahrenheitInt = round((sense.get_temperature()*9/5+32)*3**trimalInt,0)
   fTuple = toTer(fahrenheitInt)
   showTerneryRow(fTuple, trimalInt, rowInt, tritColors)

# requries from datetime import datetime
# time object -> tupple of ternary touples(hours past noon, minutes pass our, seconds past minute)
def findTime(aTime=datetime.now()):
   # make sur that time is read after the half senod point
   aTime += timedelta(seconds=.1)
   # round to the nearest second
   secFloat = aTime.second + aTime.microsecond/10**6
   if secFloat > 30: secFloat -= 60
   secInt = int(round(secFloat, 0))
   minInt = aTime.minute
   if not(aTime.minute < 30): minInt -= 60
   if secFloat < 0: minInt += 1
   hourInt = aTime.hour - 12
   if minInt + secFloat/60 < 0: hourInt += 1
   return (toTer(hourInt), toTer(minInt), toTer(secInt))
# there should b a test for this. A few times with knon correct answers could be give to the function to make the test.


# disply time in balanced ternary on pi
# requires from sense_hat import SenseHat as sense
# tuple of integers hours past noon, minutes past hour, seconds past minute,
# color tuple (a tuple of three color tuples for -1, 0, 1 colors)
# -> none (hat displays the time on its led)
def showTime (hmsTouple=findTime(datetime.now()), tritColors=((128, 0, 0), (0, 0, 0), (128, 32, 0))):
   for y in range(3):
      for x in range(4):
         if x < len(hmsTouple[y]):
            sense.set_pixel(7 - x, y, tritColors[hmsTouple[y][x]+1])
         else: sense.set_pixel (7 - x, y, (0, 0, 0))
      # clear any pixels left from previous hour
   return
# this type of function is tough to make an automated test for because it give output.
# Though a test could be made by using the pixel state function for the sense led lights.


# requires from time import sleep
# tuple of colors -> none
# refreshes time every half second.
# and should be enhaned to update time every second except for  mid minute and hour change where half second refresh is required.
# it would also be nice to have a way to stop the time. Maybe a joy
def ticer(tritColors = ((32, 0, 0), (0, 0, 0), (64, 8, 0), (0, 8, 0))):
   # sychronise with half second intervals
   zTime = datetime.now()
   sleep(1.5 - (zTime.microsecond/10**6))
   timeTuple = findTime(datetime.now())
   print ((zTime.second + zTime.microsecond/10**6, "na", timeTuple[2]))
   while(True):
      showTime(timeTuple, tritColors = tritColors)
      # put functions in a tuple to reduce the number of lines
      (showPressure(tritColors = tritColors), showHumidity(tritColors = tritColors),
         showKjeils(tritColors = tritColors), showCelcius(tritColors = tritColors),
         showFahrenheit(tritColors = tritColors), showMag(tritColors = tritColors))
      # showExK()
      # show on emulator
      sEmu.set_pixels(sense.get_pixels())
      print ((sense.get_pressure(), sense.get_humidity(), sense.get_temperature()), sense.get_compass_raw())
      
      
      
      
      
      
      
      
      
      # check for situations where the display will change in half a second
      if timeTuple[2] == (0, 1, 0, 1) or timeTuple[2] == (0, -1, 0, -1) or timeTuple == ((0, 1, 1), (0,), (0,)) or timeTuple == ((0, -1, -1), (0,), (0,)):
         zTime = datetime.now()
         timeTuple = findTime(zTime + timedelta(seconds = .5))
         sleepTime = .5 - zTime.microsecond/10**6 % .5
         if sleepTime < .25: sleepTime += .5
         print ((zTime.second + zTime.microsecond/10**6, sleepTime, timeTuple[2]))
         sleep(sleepTime)
      else:
         zTime = datetime.now()
         timeTuple = findTime(zTime + timedelta(seconds = 1))
         sleepTime = 1 - zTime.microsecond/10**6 % .5
         if sleepTime < .75: sleepTime += .5
         print ((zTime.second + zTime.microsecond/10**6, sleepTime, timeTuple[2]))
         sleep(sleepTime)
         # a function like this with no input or output is difficult to test
ticer()
