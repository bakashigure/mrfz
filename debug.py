from app.imgbb import imgbase64c
import os
import base64
from PIL import Image
from io import BytesIO

import pyautogui as pag


class idImg:
    def __init__(self):
        self.img_byte_success=base64.b64decode(imgbase64c.mission_success)
        self.img_success=Image.open(BytesIO(self.img_byte_success))

        self.img_byte_fail=base64.b64decode(imgbase64c.mission_fail)
        self.img_fail=Image.open(BytesIO(self.img_byte_fail))

        self.img_byte_start=base64.b64decode(imgbase64c.mission_start)
        self.img_start=Image.open(BytesIO(self.img_byte_start))

        self.list_suc_or_fail=[self.img_success,self.img_fail]

    def locateImg(self):
    # TODO: get screenshots of game from background
        sb=pag.locate(self.img_success,pag.screenshot(),confidence=0.7)
        if sb !=None:
            return sb
        sb=pag.locate(self.img_fail,pag.screenshot(),confidence=0.7)
    
    def locateSucOrFail(self):
        for iden in self.list_suc_or_fail:
            sb=pag.locate(iden,pag.screenshot(),confidence=0.7)
            if(sb)
            print(sb)

if __name__=='__main__':
    ttt=idImg()
    ttt.locateSucOrFail()