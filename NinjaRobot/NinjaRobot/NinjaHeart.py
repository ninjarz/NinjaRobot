import time

class NinjaHeart(object):
    def __init__(self, robot):
        self.robot = robot

    def process(self):
        while True:
            msg = self.robot.pop_group_message()
            if msg is not None:
                self.robot.send_to_group(msg.from_uin, msg.content)
            else:
                time.sleep(0.1)