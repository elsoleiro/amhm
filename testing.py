from screen import Window
import time
import math
import ctypes

x = Window('Untitled - Paint')
x.is_foreground()

'''
for i in range(500):
    ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down

    x = 100 + i*3
    y = 500 + int(math.sin(i*0.021)*100)
    s = 0.001
    ctypes.windll.user32.SetCursorPos(x,y)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up
    time.sleep(s)
'''
    

# Make functions, understand how to randomise mouse movement between
# 5 and 10 px/ms


import numpy as np
sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)

def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/
    '''
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            move_mouse(current_x:=move_x,current_y:=move_y)
    return current_x,current_y


def move_mouse(x,y):
    ctypes.windll.user32.mouse_event(2, 0, 0, 0,0) # left down
    ctypes.windll.user32.SetCursorPos(x,y)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0,0) # left up

wind_mouse(100,400,1000,400)
