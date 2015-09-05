import threading

from NinjaQueue import *
from NinjaHandler import *
from NinjaHeart import *

class NinjaRobot(object):
    def __init__(self):
        self.handler = NinjaHandle(self)
        self.handler.handler_thread = threading.Thread(target=self.handler.process)
        self.heart = NinjaHeart(self)

        # data
        self.group_msg_queue = NinjaQueue()
        pass

    def run(self):
        self.handler.login()
        handler_thread.start()

    # set
    # ----------------------------------------------------------------------------------------------------
    def push_group_message(self, msg):
        self.group_msg_queue.push(msg)

    # get
    # ----------------------------------------------------------------------------------------------------
    def get_group_message(self):
        return self.group_msg_queue.pop()

