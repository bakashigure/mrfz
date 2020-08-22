# -*- coding: utf-8 -*-

# @Time : 2019/9/26
# @Author : Twitter@bakashigure
# @Site : https://github.com/bakashigure/mrfz
# @Software: 明日方舟代肝脚本



import ctypes
import msvcrt
import re
import time
import os
import base64
import sys
from io import BytesIO
from io import TextIOWrapper
from enum import Enum
from PIL import Image
import pyautogui as pag
import win32con, win32gui, win32ui, win32api

from imgbb import imgbase64c


class IDIMG:
    game_times = 0
    game_pid = 0
    game_kind = 1
    game_title = ""

    def __init__(self):
        self.img_byte_success = base64.b64decode(imgbase64c.mission_success)
        #self.img_success = Image.open(BytesIO(self.img_byte_success))

        self.img_byte_fail = base64.b64decode(imgbase64c.mission_fail)
        #self.img_fail = Image.open(BytesIO(self.img_byte_fail))

        self.img_byte_ready = base64.b64decode(imgbase64c.mission_ready)
        #self.img_ready = Image.open(BytesIO(self.img_byte_ready))

        self.img_byte_start = base64.b64decode(imgbase64c.mission_start)
        #self.img_start = Image.open(BytesIO(self.img_byte_start))

        self.img_byte_auto_on = base64.b64decode(imgbase64c.mission_auto_on)
        #self.img_on = Image.open(BytesIO(self.img_byte_auto_on))

        self.img_byte_auto_off = base64.b64decode(imgbase64c.mission_auto_off)
        #self.img_off = Image.open(BytesIO(self.img_byte_auto_off))

        self.img_byte_playing = base64.b64decode(imgbase64c.mission_playing)
        #self.img_playing = Image.open(BytesIO(self.img_byte_playing))
        '''
        self.list_all = [
            self.img_ready,
            self.img_start,
            self.img_playing,
            self.img_success,
            self.img_fail,
        ]
        '''

        self.list_game = {
            self.img_byte_ready:'ready',
            self.img_byte_start:'start',
            self.img_byte_playing:'playing',
            self.img_byte_success:'success',
            self.img_byte_fail:'fail',
        }



    def locate(self,screenshots,width,height):
        for items,ide in self.list_game.items():
            img=Image.open(BytesIO(items))
            img=img.resize((int(width/1440*img.size[0]),int(width/1440*img.size[1])),Image.ANTIALIAS)
            if (res:=pag.locate(img,screenshots,confidence=0.7)) != None:
                print(img.size[0],img.size[1])
                print(res)
                return ide
    def locateAuto(self,screenshots,width,height):
        img=Image.open(BytesIO(self.img_byte_auto_off))
        img=img.resize((int(width/1440*img.size[0]),int(width/1440*img.size[1])),Image.ANTIALIAS)
        if(pag.locate(img,screenshots,confidence=0.7)!=None):
            return False
        return True


class GAMEKINDS(Enum):
    主线 = 1
    剿灭 = 2
    活动 = 3


class UI:
    def __init__(self, title, hwnd, kind, times):
        self.hwnd = hwnd
        self.title = title
        self.kind = kind
        self.times = times

    def update(self, current_cnt, msg):
        os.system("cls")
        self.sb = f"""
    ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟
    ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣
    ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾      明日方舟代肝脚本 Version2.0
    ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿      https://github.com/bakashigure/mrfz
    ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿
    ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿
    ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿
    ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿"


    正在监视进程: {self.hwnd}  {self.title} |  当前时间 {currentTime()}
    关卡种类: {self.kind} , 正在进行第{current_cnt+1}次，共{self.times}次
    状态:{msg}
    """
        print(self.sb)
        # sys.stdout.flush()


# 摸鱼time
def sleep(sec):
    time.sleep(sec)


# 获取当前窗口句柄
def currentHwnd():
    return win32gui.GetForegroundWindow()


# 切换进程并置顶
def switchHwnd(hwnd):
    try:
        ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
    except:
        pass
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA)
    except:
        pass
    try:
        win32api.keybd_event(13, 0, 0, 0)  # 发送一次回车事件，不然无法置顶游戏窗口 这也算是神秘bug之一吧
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass


# 当前时间
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


# 先行枚举句柄
def init():

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
        print("例子: 如您看到[   | 114514 MuMu模拟器   ]，请输入114514")
        hwnd = eval(input("请打开模拟器后重试,或手动输入hwnd(进程名前的数字):"))
        name = hwnd_title[hwnd]
        return hwnd, name

    elif n == 1:
        print("找到了一个可能是模拟器的进程[ ", game_lists[0].group(0), " ]")
        case = eval(input("是它吗? 输入1确定，输入0手动指定进程:"))
        if case == 1:
            name = hwnd_title[int(game_lists[0].group(1))]
            return game_lists[0].group(1), name
        elif case == 0:
            for h, t in hwnd_title.items():
                if t != "":
                    print(" |", "%-10s" % h, "%.50s" % t)
            hwnd = eval(input("手动输入hwnd(进程名前的数字):"))
            name = hwnd_title[hwnd]
            return hwnd, name

    elif n > 1:
        print("找到了多个包含模拟字样的进程，您可能想多开? 请手动指定进程hwnd(进程名前的数字)")
        for h, t in hwnd_title.items():
            if t != "":
                print(" |", "%-10s" % h, "%.50s" % t)
        hwnd = eval(input("手动输入hwnd(进程名前的数字):"))
        name = hwnd_title[hwnd]
        return hwnd, name

def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def getAppScreenshot(pid):
    try:
        pid = int(pid)
        left, top, right, bot = win32gui.GetWindowRect(pid)
        width = right - left
        height = bot - top
        print(
            "__log__: ",
            "left: ",
            left,
            "  top: ",
            top,
            "  right: ",
            right,
            "  bottom: ",
            bot,
        )
        print("__log__: ", "width: ", width, "  height: ", height)
        hWndDC = win32gui.GetWindowDC(pid)
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im_PIL = Image.frombuffer(
            "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1,
        )
        return im_PIL, left, width, top, height
    except:
        print("出现神必错误。")
        msvcrt.getch()
        os._exit(1)


def main():
    os.system("title 明日方舟代刷脚本V2.0 twitter@bakashigure")
    print(
        """ ####预览版本 未正式发布####
    
    欢迎使用明日方舟刷图脚本 Version2.0
    这里是一些程序说明，请仔细阅读后使用。

    0.本程序会先试图遍历进程寻找包含模拟器三字的进程，如果结果为0，则会让您自行指定进程，
       如果结果为1，则会向您确认是否为游戏进程，如果结果大于1，则会让您手动指定进程.
       随后需要您指定主线/活动关/剿灭,将游戏打开到右下角为开始行动的蓝色字样，并输入您希望循环刷图的次数.
       随后在软件内确认开始后，会自动进行识别刷图.
       游戏可以放在后台，但请不要最小化.

    1.本程序需要管理员权限，这是因为模拟鼠标点击所需，您也可以通过Github上的开源代码自己在IDE中运行.
    2.本程序支持多开，请自行指定正确的进程句柄.
    3.本软件工作原理是通过对处于后台/前台的游戏窗口进行截图并识别当前处于哪一步，不会对游戏进程进行任何的操作.
    4.建议分辨率1440*810，可以缩放窗口，但过大或过小的窗口可能造成识别失败.
    6.几乎没有错误处理，所以请不要在输入数字的地方输入其他字符.



    附1: 开源项目地址 https://github.com/bakashigure/mrfz  (请不要用于商业化)
    附2: 我的官服id 孭纸#416  (孭读mie)

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
    sb.game_pid, sb.game_title = init()
    sb.game_kind = eval(input("请输入关卡种类(1为主线，2为剿灭，3为夏活复刻[粉色开始行动字样]: "))
    sb.game_times = eval(input("请输入代刷的次数(当前体力/每关耗体): "))
    ui = UI(sb.game_pid, sb.game_title, GAMEKINDS(sb.game_kind).name, sb.game_times)

    for t in range(sb.game_times):

        while(1):
            im_PIL, left, width, top, height = getAppScreenshot(sb.game_pid)
            result=sb.locate(im_PIL,width,height)
            if result =='ready':
                x = left + width * 0.9069
                y = top + height * 0.85
                os.system("cls")
                if sb.locateAuto(im_PIL,width,height) == False:
                    ui.update(t,"您未开启代理诶，自己勾一下吧")
                    sleep(2)
                    continue
                ui.update(t, "已找到蓝色开始行动按钮，即将进行下一步")
                current_hwnd = currentHwnd()
                switchHwnd(sb.game_pid)
                sleep(1)
                pag.click(x, y)
                try:
                    switchHwnd(current_hwnd)
                except:
                    pass
                print(result)
                
                '''
                else:
                    os.system("cls")
                    ui.update(1, '请打开到右下角蓝色"开始行动"按钮，会自动识别。')
                sleep(2)
                '''

            elif result=='start':
                x = left + width * 0.8701
                y = top + height * 0.7516
                ui.update(t, "已找到红色开始行动按钮，即将进行下一步")
                current_hwnd = currentHwnd()
                switchHwnd(sb.game_pid)
                sleep(2)
                pag.click(x, y)
                try:
                    switchHwnd(current_hwnd)
                except:
                    pass
                print(result)
                sleep(1)
                
            
            elif result == 'playing':
                ui.update(t, "正在进行代理...")
                sleep(2)
            
            elif result == 'success':
                ui.update(t,"本关已完成，即将进行下一次.")
                x = left + width * 0.6657
                y = top + height * 0.5057
                current_hwnd = currentHwnd()
                switchHwnd(sb.game_pid)
                sleep(2)
                pag.click(x, y)
                try:
                    switchHwnd(current_hwnd)
                except:
                    pass
                print(result)
                sleep(1)
            
            else:
                ui.update(t,"未识别到内容，正在尝试下一次识别")
                sleep(2)
            
            


"""

 
    print(r"\
        ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟\
        ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣\
        ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾\
        ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿\
        ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿\
        ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿\
        ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿\
        ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿")



    
    gamehwnd=init()
    while(1):
        os.system("cls")
        tor,toc=readconfig()
        print("\
        ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟\n\
        ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣\n\
        ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾\n\
        ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿\n\
        ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿\n\
        ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿\n\
        ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿\n\
        ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿\n")

        print(" \n\
         _____________________________\n\
        |                             |         Tips:\n\
        |    明日方舟代刷脚本v0.04    |         欢迎使用明日方舟代刷脚本，\n\
        |    twitter@bakashigure      |         操控鼠标点击需要管理员权限，\n\
        |                             |         请确保使用管理员权限运行,\n\
        |_____________________________|         建议分辨率1440*810. \n\n")

        sleep(0.5)
        print("功能:1.单纯挂机刷(不要动鼠标) 2.边刷边看视频(体验并不好) 3.关于 4.其他输入退出\n")
        choice = eval(input("你的选择 :"))
        if choice == 1:
            
            times = eval(input("输入代刷的次数 | "))
            for i in range(times):
                if i == 0:
                    print("现在的时间", nowTime())
                    sleep(1)
                    print(r'"请将鼠标移至开始行动的"开"处，代刷将在6s后进行"')
                    sleep(6)
                    print("\n", "LINK START!  |", currentTime(), "\n")
                    pag.click()
                    gamex, gamey = pag.position()
                    pag.moveTo(gamex, gamey-50, duration=0)
                    sleep(toc)
                    pag.click()
                    print("正在代肝 ( 1 /", times, ")", "  |", currentTime())
                    sleep(tor)
                else:
                    pag.moveTo(gamex+50, gamey-500, duration=0)
                    pag.click()
                    sleep(3)
                    pag.click()
                    sleep(toc)
                    pag.moveTo(gamex, gamey, duration=0)
                    pag.click()
                    sleep(toc)
                    pag.moveTo(gamex, gamey-50, duration=0)
                    pag.click()
                    print("正在代肝 (", i+1, "/", times,")   |", currentTime())
                    sleep(tor)
            print("摸完了!              |", currentTime(), "\n", "\n")
            print("按任意键继续")
            msvcrt.getch()

        elif choice == 2:
            times = eval(input("输入代刷的次数 | "))
            for i in range(times):
                if i == 0:
                    print("现在的时间", nowTime())
                    sleep(1)
                    print("请将鼠标移至开始行动的开处，代肝将在5s后进行")
                    sleep(5)
                    gamex, gamey = pag.position()
                    print("\n", "LINK START!  |", currentTime(), "\n")
                    pag.click()
                    sleep(toc)
                    #print("游戏的句柄为",gamehwnd,"  |",currentTime())
                    pag.moveTo(gamex, gamey-50, duration=0)
                    sleep(toc)
                    pag.click()
                    #print ("START : %s" % time.ctime())
                    print("现在可以切换至其他应用,会自动切回游戏模拟点击")
                    print("正在代肝 ( 1 /", times, ")", "  |", currentTime())
                    sleep(tor)
                    nowhwnd = currentHwnd()
                    nowx, nowy = pag.position()
                    #print("现在的句柄为","  |",nowhwnd,)
                    switchHwnd(gamehwnd)
                else:
                    print("正在代肝 (", i+1, "/", times,")   |", currentTime())
                    pag.moveTo(gamex+50, gamey-500, duration=0)
                    pag.click()
                    sleep(toc)
                    pag.click()
                    sleep(toc)
                    pag.moveTo(gamex, gamey, duration=0)
                    pag.click()
                    pag.moveTo(gamex, gamey-50, duration=0)
                    sleep(toc)
                    pag.click()
                    switchHwnd(nowhwnd)
                    pag.moveTo(nowx, nowy, duration=0)
                    sleep(tor)
                    nowhwnd = currentHwnd()
                    nowx, nowy = pag.position()
                    # print("现在的句柄为",nowhwnd)
                    switchHwnd(gamehwnd)
                    # if i==(times):
                    #    break
            print("摸完了!              |", currentTime(), "\n", "\n")
            print("按任意键继续")
            msvcrt.getch()
        elif choice == 3:
            os.system("cls")
            print("\
            ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟\n\
            ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣\n\
            ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾\n\
            ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿\n\
            ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿\n\
            ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿\n\
            ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿\n\
            ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿\n\
            \n\n\
            version: 0.04\n\
            author twitter: @bakashigure\n\
            telegram: t.me/bakashigure \n\
            compile time: UTC/GMT+08:00 2020/4/30 15:45\n\
            github: https://github.com/bakashigure/mrfz\n\
            ")
            print("Press any key to continue_(:з」∠)_ ")
            msvcrt.getch()
        else:
            os._exit(1)
    """


if __name__ == "__main__":
    main()
