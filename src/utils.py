import time
def currentTime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def sleep(sec):
    return time.sleep(sec)

class ArkError(Exception):
    '''
    exception
    '''
    def __init__(self,reason):
        self.reason=str(reason)
        super(Exception,self).__init__(self,reason)
        
    def __str__(self):
        return self.reason