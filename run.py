from screen import Window
from mouse import move_mouse

target = 'Untitled - Paint'

window = Window(target)
window.is_foreground()


for i in range(10):
    move_mouse(100,400,1300,400)
