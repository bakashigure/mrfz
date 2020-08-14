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

        self.img_byte_ready=base64.b64decode(imgbase64c.mission_ready)
        self.img_ready=Image.open(BytesIO(self.img_byte_ready))

        self.img_byte_start=base64.b64decode(imgbase64c.mission_start)
        self.img_start=Image.open(BytesIO(self.img_byte_start))

        self.img_byte_auto_on=base64.b64decode(imgbase64c.mission_auto_on)
        self.img_on=Image.open(BytesIO(self.img_byte_auto_on))

        self.img_byte_auto_off=base64.b64decode(imgbase64c.mission_auto_off)
        self.img_off=Image.open(BytesIO(self.img_byte_auto_off))        

        self.list_suc_or_fail=[self.img_success,self.img_fail]
        self.list_auto_on_off=[self.img_on,self.img_off]
        self.list_ready_start=[self.img_ready,self.img_success]

        self.list_all=[self.img_success,self.img_fail,self.img_start,self.img_ready,self.img_on,self.img_off]

    def locateImg(self,imageName):
    # TODO: get screenshots of game from background
        return pag.locate(imageName,pag.screenshot(),confidence=0.7)
    
    def locateSucOrFail(self):
        for iden in self.list_suc_or_fail:
            sb=pag.locate(iden,pag.screenshot(),confidence=0.7)
            if(sb==None):
                print(sb)
    
    '''
    def locateStart(self):
        return pag.locate(self.img_start,pag.screenshot(),confidence=0.7)
    
    def locateReady(self):
        return pag.locate(self.img_ready,pag.screenshot(),confidence=0.7)

    def locateAutoOn(self):
        return pag.locate(self.img_on,pag.screenshot(),confidence=0.7)
    
    def locateAutoOff(self):
        return pag.locate(self.img_off,pag.screenshot(),confidence=0.7)

    
    '''

    def locateAll(self):
        for iden in self.list_all:
            sb=pag.locate(iden,pag.screenshot(),confidence=0.7)
            if(sb!=None):
                print(sb)
                pag.click(sb)
            
            

if __name__=='__main__':
    ttt=idImg()
    #print(ttt.locateImg(ttt.img_success))
    #ttt.locateAll()
    #im=Image.open(BytesIO(ttt.img_byte_ready))
    #im.save('23.png')
    print(ttt.list_all[2])

    