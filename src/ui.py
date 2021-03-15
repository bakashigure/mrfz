import os
from .utils import currentTime,sleep
from .log import log
class Ui:
    start_message="""
    \033[0;30;47m欢迎使用明日方舟刷图脚本 Version2.2
    这里是一些程序说明，请仔细阅读后使用.\033[0m

    0.本程序会先试图遍历进程寻找包含模拟器三字的进程，如果结果为0，则会让您自行指定进程，
       如果结果为1，则会向您确认是否为游戏进程，如果结果大于1，则会让您手动指定进程.
       随后需要您指定主线/剿灭,将游戏打开到右下角为开始行动的蓝色字样，
       勾选代理作战,随后在本程序内输入您希望循环刷图的次数.
       随后在软件内确认开始后，会自动进行识别刷图.
       游戏可以放在后台，但请不要最小化.

    1.本程序需要管理员权限，这是因为模拟鼠标点击所需，您也可以通过Github上的开源代码自己中运行.
    2.本程序支持多开，请自行指定正确的进程句柄.
    3.本软件工作原理是通过对游戏窗口进行截图并识别当前状态，不会对游戏进程进行任何的操作.
    4.建议分辨率1440*810, 缩放窗口可能造成识别失败.
    6.几乎没有错误处理，所以请不要在输入数字的地方输入其他字符.
    7.目前仅支持[简体中文]的游戏内容.
    8.建议使用雷电模拟器,mumu在某次更新之后无法正常使用该脚本.



    附0: 开源项目地址 https://github.com/bakashigure/mrfz  (请不要用于商业化)
    附1: 我的官服id 孭纸#416  (孭读mie)
    附2: contact::bakashigure@hotmail.com

    如您已阅读完毕，请按任意键继续.
    """
    @log.wrap(info="初始化ui")
    def __init__(self, title, hwnd, kind, times):
        self.hwnd = hwnd
        self.title = title
        self.kind = kind
        self.times = times
        self.log=''
        self.finish='将在完成一次后得出'
        self.start_time=0
        self.end_time=0
        self.current_cnt=0

    @log.wrap(info="更新状态")
    def update(self, current_cnt, msg):
        self.current_cnt=current_cnt
        self.log="""
    ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟
    ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣
    ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾      明日方舟代肝脚本 Version2.2 build 315.1709
    ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿      https://github.com/bakashigure/mrfz
    ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿      
    ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿      游戏窗口可以被遮挡覆盖,但请勿最小化.
    ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿      本窗口可以最小化,将在代理完成后置顶.
    ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿"


    正在监视进程: {0}  {1} |  当前时间 {2} | 预计完成时间  {3}
    关卡种类: {4} , 正在进行第{5}次，共{6}次
    状态:\033[0;30;47m {7} \033[0m
    """.format(self.hwnd,self.title,currentTime(),self.finish,self.kind,self.current_cnt+1,self.times,msg)
    def output(self):
        while(1):
            os.system("cls")
            print(self.log)
            for items in log.log:
                print(items)
            sleep(0.5)
        