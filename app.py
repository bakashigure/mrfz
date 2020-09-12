# -*- coding: utf-8 -*-

# @CreateTime : 2019/9/26
# @Author : Twitter@bakashigure
# @Site : https://github.com/bakashigure/mrfz
# @Software: 明日方舟代肝脚本


import base64
import ctypes
import msvcrt
import os
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

from imgbb import imgbase64c


class LOG:
    def __init__(self):
        self.log=[]
    def logging(self,str):
        while len(self.log)>=8:
            self.log.pop(0)
        self.log.append(str)
    def update(self,strr):
        sb="["+str(currentTime())+"] ["+strr+"]"
        return self.logging(sb)

global ll
ll=LOG()

def debug(info):
    def wrapper(func):
        def inner_wrapper(*args,**kwargs):
            sb='[{time}] [{info}] enter function {func}()'.format(
                time=currentTime(),
                info=info,
                func=func.__name__)
            ll.logging(sb)
            return func(*args,**kwargs)
        return inner_wrapper
    return wrapper


class IDIMG:
    def __init__(self):
        self.game_times = 0
        self.game_hwnd = 0
        self.game_kind = 1
        self.game_ann_kind = 1
        self.game_title = ""

        self.img_byte_success = base64.b64decode(imgbase64c.mission_success)
        self.img_success = BytesIO(self.img_byte_success)
        # self.img_success = Image.open(BytesIO(self.img_byte_success))

        self.img_byte_fail = base64.b64decode(imgbase64c.mission_fail)
        self.img_fail = BytesIO(self.img_byte_fail)
        # self.img_fail = Image.open(BytesIO(self.img_byte_fail))

        self.img_byte_ready = base64.b64decode(imgbase64c.mission_ready)
        self.img_ready = BytesIO(self.img_byte_ready)
        # self.img_ready = Image.open(BytesIO(self.img_byte_ready))

        self.img_byte_start = base64.b64decode(imgbase64c.mission_start)
        self.img_start = BytesIO(self.img_byte_start)
        # self.img_start = Image.open(BytesIO(self.img_byte_start))

        self.img_byte_auto_on = base64.b64decode(imgbase64c.mission_auto_on)
        self.img_auto_on = BytesIO(self.img_byte_auto_on)
        # self.img_on = Image.open(BytesIO(self.img_byte_auto_on))

        self.img_byte_auto_off = base64.b64decode(imgbase64c.mission_auto_off)
        self.img_auto_off = BytesIO(self.img_byte_auto_off)
        # self.img_off = Image.open(BytesIO(self.img_byte_auto_off))

        self.img_byte_playing = base64.b64decode(imgbase64c.mission_playing)
        self.img_playing = BytesIO(self.img_byte_playing)
        # self.img_playing = Image.open(BytesIO(self.img_byte_playing))

        self.img_byte_ann_chernob = base64.b64decode(imgbase64c.ann_chernob)
        self.img_ann_chernob = BytesIO(self.img_byte_ann_chernob)
        # self.img_ann_chernob=Image.open(BytesIO(self.img_byte_ann_chernob))

        self.img_byte_ann_downtown = base64.b64decode(imgbase64c.ann_downtown)
        self.img_ann_downtown = BytesIO(self.img_byte_ann_downtown)
        # self.img_ann_downtown=Image.open(BytesIO(self.img_byte_ann_downtown))

        self.img_byte_ann_outskirts = base64.b64decode(imgbase64c.ann_outskirts)
        self.img_ann_outskirts = BytesIO(self.img_byte_ann_outskirts)
        # self.img_ann_outskirts=Image.open(BytesIO(self.img_byte_ann_outskirts))

        self.img_byte_ann_success = base64.b64decode(imgbase64c.ann_success)
        self.img_ann_success = BytesIO(self.img_byte_ann_success)
        # self.imng_ann_success=Image.open(BytesIO(self.img_byte_ann_success))

        self.list_mainlinetest={
            self.img_ready:"ready",
            self.img_start:"start",
            self.img_playing:"playing",
            self.img_success:"success",
            self.img_fail:"fail",
        }

        self.list_ann_level = [
            self.img_byte_ann_chernob,
            self.img_byte_ann_downtown,
            self.img_byte_ann_outskirts,
        ]

        self.list_ann = {
            self.img_ready: "ready",
            self.img_start: "start",
            self.img_playing: "playing",
            self.img_ann_success: "success",
        }
    
        self.hwnd_title = dict()
        def getAllHwnd(hwnd,mouse):
            if (
                win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)
            ):
                self.hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        win32gui.EnumWindows(getAllHwnd, 0)

        self.game_lists = []
        for h, t in self.hwnd_title.items():
            if t != "":
                c = f"{h} {t}"
                result = re.match(r"([0-9]*) (.*)模拟器(.*)", c, flags=0)
                if result != None:
                    self.game_lists.append(result)

        if (n := len(self.game_lists)) == 0:
            for h, t in self.hwnd_title.items():
                if t != "":
                    print(" |", "%-10s" % h, "%.50s" % t)
            print("\n未找到包含'模拟器'字样的游戏进程,请手动指定进程hwnd")
            print("例子: 如您看到[   | 114514   MuMu模拟器   ]，请输入114514")
            self.game_hwnd = eval(input("\033[0;30;47m请打开模拟器后重试,或手动输入hwnd(进程名前的数字):\033[0m"))
            self.game_title = self.hwnd_title[self.game_hwnd]

        elif n == 1:
            print("找到了一个可能是模拟器的进程[ ", self.game_lists[0].group(0), " ]")
            case = eval(input("\033[0;30;47m是它吗? 输入1确定，输入0手动指定进程:\033[0m"))
            if case == 1:
                self.game_title = self.hwnd_title[int(self.game_lists[0].group(1))]
                self.game_hwnd=self.game_lists[0].group(1)
            elif case == 0:
                for h, t in self.hwnd_title.items():
                    if t != "":
                        print(" |", "%-10s" % h, "%.50s" % t)
                self.game_hwnd = eval(input("\033[0;30;47m手动输入hwnd(进程名前的数字):\033[0m"))
                self.game_title = self.hwnd_title[self.game_hwnd]
                
        elif n > 1:
            
            for h, t in self.hwnd_title.items():
                if t != "":
                    print(" |", "%-10s" % h, "%.50s" % t)
            print("\n找到了多个包含模拟字样的进程，您可能想多开? 请手动指定进程hwnd(进程名前的数字)")           
            self.game_hwnd = eval(input("\033[0;30;47m手动输入hwnd(进程名前的数字):\033[0m"))
            self.game_title= self.hwnd_title[self.game_hwnd]
            
    @debug(info="获取游戏截图")
    def getAppScreenshot(self):
        try:
            hwnd = int(self.game_hwnd)
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bot - top
            hWndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hWndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
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
            return im_PIL, left, width, top
        except:
            print("尝试截图出现错误")
            msvcrt.getch()
            os._exit(1)

    @debug(info="定位主线场景")
    def locateMainline(self):
        screenshot, _left, width, _top=self.getAppScreenshot()
        for items,value in self.list_mainlinetest.items():
            img=Image.open(items)
            img=img.resize((int(width / 1440 * img.size[0]), int(width / 1440 * img.size[1])),
                Image.ANTIALIAS,)
            if(res:=pag.locate(img,screenshot,confidence=0.95))!=None:
                position=[]
                position.append(pag.center(res)[0])
                position.append(pag.center(res)[1])
                return value,position
        return None,None

    @debug(info="定位剿灭场景")
    def locateAnn(self):
        screenshot, _left, width, _top=self.getAppScreenshot()
        for items,value in self.list_ann.items():
            img=Image.open(items)
            img=img.resize((int(width / 1440 * img.size[0]), int(width / 1440 * img.size[1])),
                Image.ANTIALIAS,)
            if(res:=pag.locate(img,screenshot,confidence=0.8))!=None:
                position=[]
                position.append(pag.center(res)[0])
                position.append(pag.center(res)[1])
                return value,position
        return None,None

    @debug(info="定位是否开启代理")
    def locateAuto(self):
        _screenshot, _left, _width, _top=self.getAppScreenshot()
        img = Image.open(self.img_auto_off)
        img = img.resize(
            (int(_width / 1440 * img.size[0]), int(_width / 1440 * img.size[1])),
            Image.ANTIALIAS,
        )
        if pag.locate(img, _screenshot, confidence=0.8) != None:
            return False
        return True


class GAMEKINDS(Enum):
    主线或材料 = 1
    剿灭 = 2
    活动 = 3
    切尔诺伯格 = 4
    龙门外环 = 5
    龙门市区 = 6


class UI:
    @debug(info="初始化ui")
    def __init__(self, title, hwnd, kind, times):
        self.hwnd = hwnd
        self.title = title
        self.kind = kind
        self.times = times
        self.log=''

    @debug(info="更新状态")
    def update(self, current_cnt, msg):
        self.log=f"""
    ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟
    ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣
    ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾      明日方舟代肝脚本 Version2.1 build0912.1528
    ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿      https://github.com/bakashigure/mrfz
    ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿      
    ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿      游戏窗口可以不置顶,但请不要最小化.
    ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿
    ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿"


    正在监视进程: {self.hwnd}  {self.title} |  当前时间 {currentTime()}
    关卡种类: {self.kind} , 正在进行第{current_cnt+1}次，共{self.times}次
    状态:\033[0;30;47m {msg} \033[0m


    """
    def output(self):
        while(1):
            os.system("cls")
            print(self.log)
            for items in ll.log:
                print(items)
            sleep(1)


# 摸鱼time
@debug("摸鱼")
def sleep(sec):
    time.sleep(sec)

# 当前时间
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

# 是否以管理员权限运行
def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

@debug("点击坐标")
def pclick(hwnd,position):
    hwnd=int(hwnd)
    p=win32api.MAKELONG(position[0],position[1])
    win32gui.SendMessage(hwnd,win32con.WM_ACTIVATE,win32con.WA_ACTIVE,0)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,p)
    sleep(0.05)
    win32api.SendMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,p)
    sleep(0.05)


# 获取当前窗口句柄
@debug("获取当前窗口句柄")
def currentHwnd():
    return win32gui.GetForegroundWindow()

# 切换进程并置顶
@debug("切换进程并置顶")
def switchHwnd(hwnd):
    hwnd=int(hwnd)
    try:
        ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
    except:
        pass
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA)
    except:
        pass
    try:
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass


def main():
    os.system("title 明日方舟代刷脚本V2.0 twitter@bakashigure")
    os.system("mode con cols=110 lines=40")
    print(
        """####预览版本 未正式发布####

    \033[0;30;47m欢迎使用明日方舟刷图脚本 Version2.0
    这里是一些程序说明，请仔细阅读后使用.\033[0m

    0.本程序会先试图遍历进程寻找包含模拟器三字的进程，如果结果为0，则会让您自行指定进程，
       如果结果为1，则会向您确认是否为游戏进程，如果结果大于1，则会让您手动指定进程.
       随后需要您指定主线/剿灭,将游戏打开到右下角为开始行动的蓝色字样，
       勾选代理作战,随后在本程序内输入您希望循环刷图的次数.
       随后在软件内确认开始后，会自动进行识别刷图.
       游戏可以放在后台，但请不要最小化.

    1.本程序需要管理员权限，这是因为模拟鼠标点击所需，您也可以通过Github上的开源代码自己在IDE中运行.
    2.本程序支持多开，请自行指定正确的进程句柄.
    3.本软件工作原理是通过对处于后台/前台的游戏窗口进行截图并识别当前状态，不会对游戏进程进行任何的操作.
    4.建议分辨率1440*810，可以缩放窗口，但过大或过小的窗口可能造成识别失败.
    6.几乎没有错误处理，所以请不要在输入数字的地方输入其他字符.
    7.目前仅支持[简体中文]的游戏内容



    附0: 开源项目地址 https://github.com/bakashigure/mrfz  (请不要用于商业化)
    附1: 我的官服id 孭纸#416  (孭读mie)
    附2: contact::bakashigure@hotmail.com

    如您已阅读完毕，请按任意键继续.
    """
    )

    msvcrt.getch()
    os.system("cls")

    if isAdmin():
        pass
    else:
        print("鼠标点击需要管理员权限，请以管理员权限运行重试.")
        print("按任意键退出.")
        msvcrt.getch()
        os._exit(1)

    sb = IDIMG()
    sb.game_kind = eval(input("\033[0;30;47m请输入关卡种类:  1.[主线/材料]   2.[剿灭] \033[0m"))
    con_hwnd=currentHwnd()
    if sb.game_kind == 2:
        sb.game_ann_kind = eval(input("\033[0;30;47m请输入剿灭关卡:  1.[切尔诺伯格]   2.[龙门外环]   3.[龙门市区]\033[0m"))
    sb.game_times = eval(input("\033[0;30;47m请输入代刷的次数(当前体力/每关耗体): \033[0m"))
    print("请将游戏打开至'右下角蓝色开始行动',会自动识别.")
    sleep(3)
    if sb.game_kind == 1:
        ui = UI(sb.game_hwnd, sb.game_title, GAMEKINDS(sb.game_kind).name, sb.game_times)
    else:
        _gamekinds = (
            str(GAMEKINDS(sb.game_kind).name)
            + "-"
            + str(GAMEKINDS(sb.game_ann_kind + 3).name)
        )
        ui = UI(sb.game_hwnd, sb.game_title, _gamekinds, sb.game_times)

    thread_log=threading.Thread(target=ui.output)
    thread_log.start()
    for t in range(sb.game_times):
        while 1:
            if sb.game_kind == 1:
                result,position = sb.locateMainline()

                if result==None:
                    ui.update(t, "未识别到内容，正在尝试下一次识别")
                    sleep(2)

                elif result == "ready":
                    if (
                        sb.locateAuto()== False
                    ):
                        ui.update(t, "您未开启代理诶，自己勾一下吧")
                        ll.update("定位代理")
                        sleep(2)
                        continue
                    ui.update(t, "已找到蓝色开始行动按钮,即将进行下一步")
                    ll.update("定位蓝色开始行动")
                    pclick(sb.game_hwnd,position)
                    sleep(2)

                elif result == "start":
                    ui.update(t, "已找到红色开始行动按钮,即将进行下一步")
                    ll.update("定位红色开始行动")
                    pclick(sb.game_hwnd,position)
                    sleep(2)

                elif result == "playing":
                    ui.update(t, "代理指挥作战正常运行中...")
                    ll.update("代理指挥正常运行")
                    sleep(2)

                elif result == "success":
                    ui.update(t, "本关已完成，即将进行下一次.")
                    ll.update("本关已完成")
                    pclick(sb.game_hwnd,position)
                    sleep(4)
                    break
            
            elif sb.game_kind == 2:
                result,position = sb.locateAnn()
                if result==None:
                    ui.update(t, "未识别到内容，正在尝试下一次识别")
                    sleep(2)

                elif result == "ready":
                    if (
                        sb.locateAuto()== False
                    ):
                        ui.update(t, "您未开启代理诶，自己勾一下吧")
                        ll.update("定位代理")
                        sleep(2)
                        continue
                    ui.update(t, "已找到蓝色开始行动按钮，即将进行下一步")
                    ll.update("定位蓝色开始行动")
                    pclick(sb.game_hwnd,position)
                    sleep(2)

                elif result == "start":
                    ui.update(t, "已找到红色开始行动，即将进行下一步")
                    ll.update("定位红色开始行动")
                    pclick(sb.game_hwnd,position)
                    sleep(2)

                elif result == "playing":
                    ui.update(t, "代理指挥作战正常运行中...")
                    ll.update("代理指挥正常运行")
                    sleep(2)

                elif result == "success":
                    ui.update(t, "本关已完成，即将进行下一次.")
                    pclick(sb.game_hwnd,position)
                    sleep(4)
                    pclick(sb.game_hwnd,position)
                    sleep(4)
                    break

    ui.update(t, "本次代理指挥作战已全部完成，感谢使用!")
    try:
        switchHwnd(con_hwnd)
    except:
        pass
    msvcrt.getch()


if __name__ == "__main__":
    main()
