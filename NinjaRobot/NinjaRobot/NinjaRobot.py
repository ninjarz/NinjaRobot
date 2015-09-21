import threading

from NinjaQueue import *
from NinjaHandler import *
from NinjaHeart import *
from NinjaCommand import *

class NinjaRobot(object):
    def __init__(self):
        self.handler = NinjaHandle(self)
        self.handler_thread = threading.Thread(target=self.handler.process)
        self.heart = NinjaHeart(self)
        self.heart_thread = threading.Thread(target=self.heart.process)
        self.command = NinjaCommand(self)

        # data
        self.group_msg_queue = NinjaQueue()
        pass

    # ----------------------------------------------------------------------------------------------------
    def run(self):
        self.handler.login()
        self.handler_thread.start()
        self.heart_thread.start()
        self.command.process()

    # data
    # ----------------------------------------------------------------------------------------------------
    def load_config(self):
        load_config()

    def load_dict(self):
        self.heart.load_dict()

    def save_dict(self):
        self.heart.save_dict()

    def load_reply(self):
        self.heart.load_reply()

    def push_group_message(self, msg):
        self.group_msg_queue.push(msg)

    def pop_group_message(self):
        return self.group_msg_queue.pop()

    # handler
    # ----------------------------------------------------------------------------------------------------
    def send_to_group(self, uin, msg):
        self.handler.send_to_group(uin, msg)

    # heart
    # ----------------------------------------------------------------------------------------------------
    def load_reply(self):
        self.heart.load_reply()



