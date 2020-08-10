# coding=utf-8
import os
import base64
import pyautogui as pag
from PIL import Image
from io import BytesIO

from app.imgbb import imgbase64c




# 识别方舟测试

class idImg:
    def __init__(self):
        self.img_byte_success=base64.b64decode(imgbase64c.mission_success)
        self.img_success=Image.open(BytesIO(self.img_byte_success))

        self.img_byte_fail=base64.b64decode(imgbase64c.mission_fail)
        self.img_fail=Image.open(BytesIO(self.img_byte_fail))

        self.img_byte_start=base64.b64decode(imgbase64c.mission_start)
        self.img_start=Image.open(BytesIO(self.img_byte_start))


sb=idImg()

#pag.locate()

location=pag.locateOnScreen(sb.img_success,confidence=0.4)
print(location)
