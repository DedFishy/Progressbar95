import win32api # type: ignore
import win32con # type: ignore
import win32gui # type: ignore
from ctypes import windll, Structure, c_long, byref
from colors import transparent

def config_win32_window(hwnd):
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def calculate_center_positioning(container_size, child_size):
    return [
        container_size[0]/2 - child_size[0]/2,
        container_size[1]/2 - child_size[1]/2
    ]