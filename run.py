from screen import Window
from mouse import next_point

def main():
    target = 'Untitled - Paint'

    window = Window(target)

    window.is_foreground()

    for i in range(10):
        next_point(100,400,1300,400)

if __name__ == '__main__':
    main()
