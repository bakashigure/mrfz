from .utils import currentTime
import time


class Log:
    def __init__(self):
        self.log = []

    def wrap(self,info):
        def wrapper(func):
            def inner_wrapper(*args, **kwargs):
                sb = '[{0}] [{1}] enter function {2}()'.format(currentTime(),info,func.__name__)
                log.logging(sb)
                return func(*args, **kwargs)
            return inner_wrapper
        return wrapper

    def logging(self, str):
        while len(self.log) >= 10:
            self.log.pop(0)
        self.log.append(str)

    def update(self,strr):
        sb="[{0}] [{1}]".format(str(currentTime()),strr)
        return self.logging(sb)

log=Log()




@log.wrap("摸鱼")
def sleep(sec):
    time.sleep(sec)





