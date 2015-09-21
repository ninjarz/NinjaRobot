
class NinjaCommand(object):
    def __init__(self, robot):
        self.robot = robot

    # ----------------------------------------------------------------------------------------------------
    def process(self):
        while True:
            content = input('')
            if content == 'load config':
                self.robot.load_config()
            elif content == 'load dict':
                self.robot.load_dict()
            elif content == 'save dict':
                self.robot.save_dict()
            elif content == 'load reply':
                self.robot.load_reply()
            else:
                print('invalid command!')