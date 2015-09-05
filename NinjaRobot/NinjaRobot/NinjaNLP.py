import json
import random

from Config import *

class NinjaNLP(object):
    def __init__(self):
        self.reply_data = {}
        self.load_reply()
        pass

    # ----------------------------------------------------------------------------------------------------
    def load_reply(self):
        try:
            fin = open(config['nlp_data_path'], 'r')
            self.reply_data = json.loads(fin.read())
            fin.close()
        except:
            print('Load reply data fail!')
            return

    def parse(self, sentence):
        unknown_list = self.reply_data['unknown']
        num = len(unknown_list)
        if num != 0:
            return unknown_list[random.randint(0, num - 1)]
        return '• ^ •'