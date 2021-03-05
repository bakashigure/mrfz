import time
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def sleep(sec):
    return time.sleep(sec)

def HwndNotFoundException(Exception):
    return "hwnd not found"

def ScreenshotException(Exception):
    return "get screenshot failed"