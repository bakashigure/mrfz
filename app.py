# -*- coding: utf-8 -*-

# @Time : 2019/9/26
# @Author : twitter@bakashigure
# @Site : https://github.com/bakashigure/mrfz
# @Software: 明日方舟代肝脚本

import ctypes
import msvcrt
import re
import time
import os

import pyautogui as pag
import win32con
import win32gui


# 摸鱼time
def sleep(sec):
    time.sleep(sec)

# 获取当前窗口句柄
def currentHwnd():
    return win32gui.GetForegroundWindow()

# 切换进程并置顶
def switchHwnd(hwnd):
    ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNA)
    win32gui.SetForegroundWindow(hwnd)
    return None

# 当前时间带日期
def nowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

# 当前时间不带日期
def currentTime():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))



# 先行枚举句柄
def init():
    os.system("title 明日方舟代刷脚本v0.04 twitter@bakashigure")
    hwnd_title = dict()
    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t is not "":
            c = (f'{h} {t}')
            result = re.match(r'[0-9]* (.*)模拟器(.*)', c, flags=0)
            if result != None:
                gamehwndd = eval(re.sub(r"\D", "", result.group(0)))
                print("获取到游戏句柄 |",gamehwndd)
                sleep(1)
                break
    else:
        print("未找到游戏进程,请确保有一个进程名包含\'模拟器\',例如\'MuMu模拟器\'")
        print("请打开模拟器后重试,按任意键退出程序", "\n")
        msvcrt.getch()
        os._exit(1)
    return gamehwndd


# 弱智编译器


# 读取配置文件
def readconfig():
    tor=130
    toc=3
    #tor为 time of round 每局所花费的时间
    #toc为 time of click 每次点击间隔，考虑网络延时及系统性能，设置了一个较大的值
    ''' 
    #怪麻烦的 写死算了
    with open(r'./config.txt', 'r') as cfg:
        list1 = cfg.readlines()
        tor = int(
            re.match(r'Time_Of_EveryRound:"([0-9]*)"', list1[0], flags=0).group(1))
        toc = int(
            re.match(r'Time_Of_EveryClick:"([0-9]*)"', list1[1], flags=0).group(1))
    '''
    return tor,toc


def main():
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
                    #print ("Start : %s" % time.ctime())
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


if __name__ == '__main__':
    main()
