import datetime
import base64
import ctypes
import os

import inspect
import re
import sys
import threading
import time
from enum import Enum
from io import BytesIO, TextIOWrapper

import pyautogui as pag
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

def getAppScreenshot(hwnd):
    hwnd = int(game_hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    print(width,height)
    hWndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC,
                    (0, 0), win32con.SRCCOPY)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im_PIL = Image.frombuffer(
        "RGB",
        (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
        bmpstr,
        "raw",
        "BGRX",
        0,
        1,
    )
    # be careful of memory leak - -, win32 make it shit
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    return im_PIL,  width, height


hwnd_title = dict()

def getAllHwnd(hwnd, mouse):
    if (
        win32gui.IsWindow(hwnd)
        and win32gui.IsWindowEnabled(hwnd)
        and win32gui.IsWindowVisible(hwnd)
    ):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(getAllHwnd, 0)




game_lists = []
for h, t in hwnd_title.items():
    if t != "":
        c = f"{h} {t}"
        result = re.match(r"([0-9]*) (.*)模拟器(.*)", c, flags=0)
        if result != None:
            game_lists.append(result)

if (n := len(game_lists)) == 0:
    for h, t in hwnd_title.items():
        if t != "":
            print(" |", "%-10s" % h, "%.50s" % t)
    print("\n未找到包含'模拟器'字样的游戏进程,请手动指定进程hwnd")
    print("例子: 如您看到[   | 114514   MuMu模拟器   ]，请输入114514")
    game_hwnd = eval(
        input("\033[0;30;47m请打开模拟器后重试,或手动输入hwnd(进程名前的数字):\033[0m"))
    game_title = hwnd_title[game_hwnd]

elif n == 1:
    print("找到了一个可能是模拟器的进程[ ", game_lists[0].group(0), " ]")
    case = eval(input("\033[0;30;47m是它吗? 输入1确定，输入0手动指定进程:\033[0m"))
    if case == 1:
        game_title = hwnd_title[int(
            game_lists[0].group(1))]
        game_hwnd = game_lists[0].group(1)
    elif case == 0:
        for h, t in hwnd_title.items():
            if t != "":
                print(" |", "%-10s" % h, "%.50s" % t)
        game_hwnd = eval(
            input("\033[0;30;47m手动输入hwnd(进程名前的数字):\033[0m"))
        #game_title = hwnd_title[game_hwnd]
        game_title = ''


while 1:
    time.sleep(0.5)
    print("  ")
    _pil,w,h=getAppScreenshot(game_hwnd)
    img=Image.open("E:\Code\python\pytrain\mrfz\src\img\ms.png")
    radio= ((h-36)/810)
    _w=int(radio*img.size[0])
    _h=int(radio*img.size[1])

    print(img.size[0]," ",img.size[1])
    img.resize((_w,_h))
    print(_w," ",_h)
    print(img.size[0]," ",img.size[1])

    if pag.locate(img,_pil,confidence=0.8):
        print('found')