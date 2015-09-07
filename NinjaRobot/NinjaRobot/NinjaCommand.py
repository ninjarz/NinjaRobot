
class NinjaCommand(object):
    def __init__(self, robot):
        self.robot = robot

    # ----------------------------------------------------------------------------------------------------
    def process(self):
        while True:
            content = input('')
            if content == 'reload':
                self.robot.load_reply()
            else:
                print('invalid command!')