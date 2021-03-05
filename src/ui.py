import os
from .utils import currentTime,sleep
from .log import log
class Ui:
    @log.wrap(info="初始化ui")
    def __init__(self, title, hwnd, kind, times):
        self.hwnd = hwnd
        self.title = title
        self.kind = kind
        self.times = times
        self.log=''
        self.finish='将在完成一次后得出'

    @log.wrap(info="更新状态")
    def update(self, current_cnt, msg):
        self.log=f"""
    ⣿⣿⡟⠁⠄⠟⣁⠄⢡⣿⣿⣿⣿⣿⣿⣦⣼⢟⢀⡼⠃⡹⠃⡀⢸⡿⢸⣿⣿⣿⣿⣿⡟
    ⣿⣿⠃⠄⢀⣾⠋⠓⢰⣿⣿⣿⣿⣿⣿⠿⣿⣿⣾⣅⢔⣕⡇⡇⡼⢁⣿⣿⣿⣿⣿⣿⢣
    ⣿⡟⠄⠄⣾⣇⠷⣢⣿⣿⣿⣿⣿⣿⣿⣭⣀⡈⠙⢿⣿⣿⡇⡧⢁⣾⣿⣿⣿⣿⣿⢏⣾      明日方舟代肝脚本 Version2.2 build --
    ⣿⡇⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⠇⠄⠄⢿⣿⡇⢡⣾⣿⣿⣿⣿⣿⣏⣼⣿      https://github.com/bakashigure/mrfz
    ⣿⣷⢰⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣧⣀⡄⢀⠘⡿⣰⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿      
    ⢹⣿⢸⣿⣿⠟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣉⣤⣿⢈⣼⣿⣿⣿⣿⣿⣿⠏⣾⣹⣿⣿      游戏窗口可以被遮挡覆盖,但请勿最小化.
    ⢸⠇⡜⣿⡟⠄⠄⠄⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣻⣿⣿⣿⣿⣿⠟⠁⢳⠃⣿⣿⣿
    ⠄⣰⡗⠹⣿⣄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⠟⣅⣥⣿⣿⣿⣿⠿⠋⠄⠄⣾⡌⢠⣿⡿"


    正在监视进程: {0}  {1} |  当前时间 {2} | 预计剩余时间  {3}
    关卡种类: {4} , 正在进行第{5}次，共{6}次
    状态:\033[0;30;47m {7} \033[0m
    """.format(self.hwnd,self.title,currentTime(),self.finish,self.kind,current_cnt+1,self.times,msg)
    def output(self):
        while(1):
            os.system("cls")
            print(self.log)
            for items in log.log:
                print(items)
            sleep(0.5)
        