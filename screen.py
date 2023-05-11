import win32gui
import win32ui
import ctypes
from PIL import Image
global user32
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)


class Window:
    def __init__(self, window):
        self.name = window
        self.hwnd = win32gui.FindWindow(None, window)
        self.hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        self.dc = win32ui.CreateDCFromHandle(self.hwnd_dc)
        self.s_dc = self.dc.CreateCompatibleDC()
        self.left, self.top, self.right, self.bottom = win32gui.GetClientRect(self.hwnd)
        self.width, self.height = (self.right - self.left), (self.bottom - self.top)

    def is_foreground(self):
        other_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if  other_window != self.name:
            win32gui.SetForegroundWindow(self.hwnd)

    def destroy(self):
        self.s_dc.DeleteDC()
        self.dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwnd_dc)

    def save_screenshot(self):
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(self.dc, self.width, self.height)
        self.s_dc.SelectObject(bitmap)

        screen = user32.PrintWindow(self.hwnd, self.s_dc.GetSafeHdc(), 1)
        bitmap_info = bitmap.GetInfo()
        bitmap_bits = bitmap.GetBitmapBits(True)

        if bool(screen):
            im = Image.frombuffer(
                'RGB',
                (bitmap_info['bmWidth'], bitmap_info['bmHeight']),
                bitmap_bits, 'raw', 'BGRX', 0, 1)
            im.save('images/screen.jpg')
            win32gui.DeleteObject(bitmap.GetHandle())
            self.destroy()
            return True
        else:
            raise Exception("Unable to take screenshot, breaking!")


x = Window('Untitled - Paint')
x.save_screenshot()
x.is_foreground()
