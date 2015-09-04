import os
import time
import datetime
import random

from Config import *
from NinjaHTTP import *


class NinjaHandle(object):
    def __init__(self):
        self.request = NinjaHTTP()

        self.ptwebqq = ''
        self.vfwebqq = ''
        self.client_id = int(random.uniform(11111111, 88888888))
        self.psession_id = ''
        self.msg_id = int(random.uniform(11111111, 88888888))

        # info
        self.id_map = {}

        pass

    def login(self):
        # login msg
        # ----------------------------------------------------------------------------------------------------
        # load page
        page_str = self.request.get(config['smart_qq_url'])
        # find login url
        login_url = self.get_page_info(page_str, r'\.src = "(.+?)"')
        page_str = self.request.get(login_url + '0')
        # appid
        appid = self.get_page_info(page_str, r'var g_appid =encodeURIComponent\("(\d+)"\);')
        print(appid)
        # sign
        sign = self.get_page_info(page_str, r'var g_login_sig=encodeURIComponent\("(.+?)"\);')
        print(sign)
        # js_ver
        js_ver = self.get_page_info(page_str, r'var g_pt_version=encodeURIComponent\("(\d+)"\);')
        print(js_ver)
        # mibao_css
        mibao_css = self.get_page_info(page_str, r'var g_mibao_css=encodeURIComponent\("(.+?)"\);')
        print(mibao_css)

        # login
        # ----------------------------------------------------------------------------------------------------
        start_time = int(time.mktime(datetime.datetime.utcnow().timetuple())) * 1000
        # download qrcode
        self.request.download(config['qrcode_url'].format(appid), config['qrcode_path'])
        # verification
        while True:
            current_time = int(time.mktime(datetime.datetime.utcnow().timetuple())) * 1000
            page_str = self.request.get(config['qrcode_login_url'].format(appid, current_time - start_time, mibao_css, js_ver, sign), Referer=login_url)
            print('login result:', page_str)
            result = page_str.split("'")
            if result[1] == '65':
                self.request.download(config['qrcode_url'].format(appid), config['qrcode_path'])
            elif result[1] == '0':
                # delete qrcode
                if os.path.exists(config['qrcode_path']):
                    os.remove(config['qrcode_path'])
                # load wait page
                page_str = self.request.get(result[5])
                url = self.get_page_info(page_str, r' src="(.+?)"')
                if url != '':
                    page_str = self.request.get(url.replace('&amp;', '&'))
                    url = self.get_page_info(page_str, r'location\.href="(.+?)"')
                    page_str = self.request.get(url)
                break
            time.sleep(2)
        self.ptwebqq = self.request.get_cookie('ptwebqq')
        print('ptwebqq:', self.ptwebqq)
        # authorize
        while True:
            params = {
                'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(self.ptwebqq, self.client_id, self.psession_id),
            }
            page_str = self.request.post(config['qrcode_authorize_url'], params, Referer=config['referer'])
            if page_str == '':
                time.sleep(2)
                continue
            print('authorize result:', page_str)
            result = json.loads(page_str)
            if result['retcode'] != 0:
                break
            # success
            self.vfwebqq = result['result']['vfwebqq']
            self.psession_id = result['result']['psessionid']
            print('login success')
            return True

    def process(self):
        # get msg
        # ----------------------------------------------------------------------------------------------------
        while True:
            params = {
                'r': '{{"psessionid":"{0}","ptwebqq":"{1}","clientid":{2},"key":""}}'.format(self.psession_id, self.ptwebqq, self.client_id)
            }
            page_str = self.request.post(config['msg_url'], params, Referer=config['referer'])
            if page_str == '':
                time.sleep(0.1)
                continue
            # print('msg:', page_str)
            result = json.loads(page_str)

            # empty
            if result['retcode'] == 102:
                continue
            # update ptwebqq
            elif result['retcode'] == 116:
                self.ptwebqq = result['p']
                continue
            elif result['retcode'] == 102:
                continue
            # msg
            elif result['retcode'] == 0:
                result = result['result'][0]
                msg_type = result['poll_type']
                if msg_type in self.__dict__:
                    self.__dict__[msg_type].__get__(self, NinjaHandle)(result)
            else:
                continue

    # get
    # ----------------------------------------------------------------------------------------------------
    def message(self):
        pass

    def sess_message(self):
        pass

    def group_message(self, msg):
        group_uin = msg['value']['from_uin']
        self.send_to_group(group_uin, 'xixi')
        pass

    def discu_message(self):
        pass

    def kick_message(self):
        pass

    def buddies_status_change(self):
        pass

    def input_notify(self):
        pass

    def tips(self):
        pass

    # send
    # ----------------------------------------------------------------------------------------------------
    def send_to_group(self, uin, msg):
        r_info = {
            "group_uin": uin,
            "content": '[\"{0}\",[\"font\",{{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}}]]'.format(msg),
            "face": 588,
            "clientid": self.client_id,
            "msg_id": self.msg_id,
            "psessionid": self.psession_id
        }
        params = {
            'r': json.dumps(r_info),
        }
        page_str = self.request.post(config['send_group_url'], params, Referer=config['referer'])
        self.msg_id += 1

    def get_id(self, uin):
        page_str = self.request.get(config['get_uin_url'].format(uin, self.vfwebqq), Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        if result['retcode'] != 0:
            return False
        print("id info:", result)
        self.id_map[uin] = result['result']['account']
        return True

    # tools
    # ----------------------------------------------------------------------------------------------------
    @staticmethod
    def get_page_info(page, pattern):
        result = re.search(pattern, page)
        if result is None:
            return ''
        return result.group(1)

