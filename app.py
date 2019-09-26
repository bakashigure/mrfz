# -*- coding: utf-8 -*-

#@Time : 2019/9/26
#@Author : twitter@bakashigure
#@Site : https://github.com/bakashigure/mrfz
#@Software: 明日方舟代肝脚本

import pyautogui as pag
import time
import win32gui
import win32con
import ctypes
import re
import msvcrt

#摸鱼time
def sleep(timeeee):
    time.sleep(timeeee)

#获取当前窗口句柄
def currenthwnd():
    return win32gui.GetForegroundWindow()

# 切换进程并置顶
def switchhwnd(hwnd): 
    ctypes.windll.user32.SwitchToThisWindow(hwnd,True)
    win32gui.ShowWindow(hwnd,win32con.SW_SHOWNA)
    win32gui.SetForegroundWindow(hwnd)
    return None

#遍历所有句柄 
hwnd_title = dict()
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(get_all_hwnd, 0)

#当前时间
def NowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def CurrentTime():
    return time.strftime('%H:%M:%S',time.localtime(time.time()))


print(" _____________________________")
print("|                             |")
print("|    明日方舟代刷脚本v0.01    |")
print("|    twitter@bakashigure      |")
print("|                             |")
print("|_____________________________|","\n\n")


#获取游戏句柄
for h,t in hwnd_title.items():
  if t is not "":
    c=(f'{h} {t}')
    error=1
    result=re.match(r'[0-9]* (.*)模拟器',c,flags=0)
    if result != None:
        gamehwnd=eval(re.sub(r"\D","",result.group(0)))
        print("获取到游戏句柄 |",gamehwnd)
        error=0
        break

if error==1:
    print("未找到游戏进程,请确保有一个进程名包含(模拟器)")
    print("请打开模拟器后重试,按任意键退出程序","\n")
    msvcrt.getch()
    exit()

#输入代肝次数
times=eval(input("输入代肝的次数 | "))
#每回合消耗的时间
timee=eval(input("输入每回合消耗的时间，建议设置120 | "))

for i in range(times):
     if i ==0:
        print("现在的时间",NowTime())
        #print ("Start : %s" % time.ctime())
        sleep(1)
        print("请将鼠标移至开始行动的开处，代肝将在5s后进行")
        sleep(5)
        gamex,gamey = pag.position()
        print("\n","LINK START!  |",CurrentTime(),"\n")
        pag.click()
        sleep(1)
        #print("游戏的句柄为",gamehwnd,"  |",CurrentTime())
        pag.moveTo(gamex,gamey-50,duration=0)
        sleep(1)
        pag.click()
        #print ("Start : %s" % time.ctime())
        print("现在可以切换至其他应用,会自动切回游戏模拟点击")
        print("正在代肝 ( 1 /",times,")","  |",CurrentTime())
        sleep(timee)
        nowhwnd=currenthwnd()
        nowx,nowy=pag.position()
        #print("现在的句柄为","  |",nowhwnd,)
        switchhwnd(gamehwnd)
     else:
        print("正在代肝 (",i+1,"/",times,")","  |",CurrentTime())
        pag.moveTo(gamex,gamey,duration=0)
        pag.click()
        sleep(3)
        pag.click()
        pag.moveTo(gamex,gamey-50,duration=0)
        sleep(1)
        pag.click()
        switchhwnd(nowhwnd)
        pag.moveTo(nowx,nowy,duration=0)
        sleep(timee)
        nowhwnd=currenthwnd()
        nowx,nowy=pag.position()
        #print("现在的句柄为",nowhwnd)
        switchhwnd(gamehwnd)
        #if i==(times):
        #    break

print("摸完了!              |",CurrentTime(),"\n","\n")
print("按任意键退出程序")
msvcrt.getch()







