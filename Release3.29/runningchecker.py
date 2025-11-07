def is_already_running():
    from ctypes import windll, wintypes
    return windll.user32.FindWindowW(0, titleofprogramme)