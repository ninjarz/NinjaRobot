import time

from Config import *
from NinjaNLP import *

class NinjaHeart(object):
    def __init__(self, robot):
        self.robot = robot
        self.nlp = NinjaNLP()

    # ----------------------------------------------------------------------------------------------------
    def process(self):
        while True:
            msg = self.robot.pop_group_message()
            if msg is not None:
                self.robot.send_to_group(msg.from_uin, self.nlp.parse(msg.content))
            else:
                time.sleep(config['heart_speed'])

    # NLP
    # ----------------------------------------------------------------------------------------------------
    def load_dict(self):
        self.nlp.load_dict()

    def load_reply(self):
        self.nlp.load_reply()