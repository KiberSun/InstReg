import PIL as pil
import mss
import cv2 as cv
import time
import numpy as np
import pyautogui as gui
import pytesseract as tes
from pytesseract import pytesseract


def waiting(seconds : int):
    for i in range (seconds, 0, -1):
        print("You have " + str(i) + " seconds to open instagram login page in your browser")
        time.sleep(1)
    print("times up")


def infield(a, x):
    ok = True
    for i in range (x - 5, x + 5, 1):
        ok = ok and a[i]
    return ok

tes.pytesseract.tesseract_cmd = r'<Your path to tesseract.exe>'
waiting(3)
screensize = gui.size()
frame = {"top": 0, "bot": screensize.height, "left": 0, "right": screensize.width}
if (str(screensize) == "Size(width=1366, height=768)"):
    frame = {"top": 120, "bot": 720, "left": 290, "right": 1060}

sct = mss.mss()
image = sct.grab({"top": frame["top"], "left": frame["left"], "width": frame["right"] - frame["left"], "height": frame["bot"] - frame["top"]})
bgrpixels = np.array(image)
pixels = cv.cvtColor(bgrpixels, cv.COLOR_BGR2RGB)

lowmask1 = np.array([0, 130, 220])
highmask1 = np.array([20, 170, 255])
lowmask2 = np.array([90, 140, 240])
highmask2 = np.array([110, 160, 255])

mask1 = cv.inRange(pixels, lowmask1, highmask1)
mask2 = cv.inRange(pixels, lowmask2, highmask2)
mask = mask1 + mask2


word = tes.image_to_string(mask, lang='rus', config='--psm 6')
letters = tes.image_to_boxes(mask, lang='rus', config='--psm 6')

print(word)
print()
print(letters)

numofsym = 0
if ('Войти' in word):
   numofsym = 5

locationstring = letters.split('\n')
locationstring = locationstring[numofsym].split(' ')
x = (int(locationstring[3]) + int(locationstring[1])) / 2 + frame["left"]
y = frame["bot"] - (int(locationstring[2]) + int(locationstring[4])) / 2
 
print()
print(locationstring)
print()
print(x)
print(y)

gui.moveTo(x, y, 0.1)
gui.mouseDown()
time.sleep(0.1)
gui.mouseUp()

time.sleep(2)

image = sct.grab({"top": frame["top"], "left": frame["left"], "width": frame["right"] - frame["left"], "height": frame["bot"] - frame["top"]})
bgrpixels = np.array(image)
pixels = cv.cvtColor(bgrpixels, cv.COLOR_BGR2RGB)

lowmask1 = np.array([249, 249, 249])
highmask1 = np.array([251, 251, 251])
mask = cv.inRange(pixels, lowmask1, highmask1)

print(mask)

leftborder = 0
rightborder = frame["right"] - frame["left"]
j = 0
for i in mask[0]:
    print(i)
    if i == 0 and leftborder == 0:
        leftborder = j
    if i == 0:
        rightborder = j
    j += 1

x = int(leftborder + (rightborder - leftborder) * 7 / 10) + 1


a = []
for i in range(0, len(mask) - 1, 1):
    a.append(mask[i, x] == 255)

y = [0, 0, 0, 0]
print(a)
numofdetect = 0
detected = False
for i in range(40, len(a) - 20, 1):
    if infield(a, i) and not detected:
        detected = True
        y[numofdetect] = i
        numofdetect += 1
    if not a[i]:
        detected = False
    if numofdetect == 4:
        break

print(y)


address = 'address' 
name = 'name'
username = 'username'
password = 'password'


gui.moveTo(frame["left"] + x, frame["top"] + y[3])
gui.click()
time.sleep(0.2)
gui.write(password)

gui.moveTo(frame["left"] + x, frame["top"] + y[2])
gui.click()
time.sleep(0.2)
gui.write(username)

gui.moveTo(frame["left"] + x, frame["top"] + y[1])
gui.click()
time.sleep(0.2)
gui.write(name)

gui.moveTo(frame["left"] + x, frame["top"] + y[0])
gui.click()
time.sleep(0.2)
gui.write(address)

