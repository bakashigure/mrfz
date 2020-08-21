import sys
import time
from enum import Enum



class gameKinds(Enum):
    主线=1
    剿灭=2
    活动关=3


def currentTime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

print(currentTime())

print(type(currentTime()))
