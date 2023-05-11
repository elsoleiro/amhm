import cv2 as cv
import numpy as np
import win32api
import win32con

import win32gui
import win32ui
import ctypes
from PIL import Image


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

hwnd = win32gui.FindWindow(None, 'Runelite')
left, top, right, bottom = win32gui.GetClientRect(hwnd)
# Where GetClientRect is the location of the window on the screen

width, height = (right-left), (bottom-top)
# Which is the size of the window from hwnd

hwnd_dc = win32gui.GetWindowDC(hwnd)

device_context = win32ui.CreateDCFromHandle(hwnd_dc)
save_dc = device_context.CreateCompatibleDC()

bitmap = win32ui.CreateBitmap()
bitmap.CreateCompatibleBitmap(device_context, width, height)
save_dc.SelectObject(bitmap)

result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 1)

bitmap_info = bitmap.GetInfo()
bitmap_bits = bitmap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bitmap_info['bmWidth'], bitmap_info['bmHeight']),
    bitmap_bits, 'raw', 'BGRX', 0, 1)
im.save('bg.jpg')

win32gui.DeleteObject(bitmap.GetHandle())
save_dc.DeleteDC()
device_context.DeleteDC()
win32gui.ReleaseDC(hwnd, hwnd_dc)


'''
bg = cv.imread('bg.jpg', cv.IMREAD_UNCHANGED)
bg2 = cv.imread('bg2.jpg', cv.IMREAD_UNCHANGED)
width, height = Image.open('bg2.jpg').size


result = cv.matchTemplate(bg, bg2, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

max_loc = (int(max_loc[0]+(width/2)), int(max_loc[1]+(height/2)))

win32api.SetCursorPos(max_loc)

cv.imshow('Result', result)
cv.waitKey()
'''
