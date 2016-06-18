import os
import time
import datetime
import random

from Config import *
from NinjaHTTP import *


class NinjaHandle(object):
    def __init__(self, robot):
        self.robot = robot
        self.request = NinjaHTTP()

        self.cip = 0
        self.uin = 0
        self.ptwebqq = ''
        self.vfwebqq = ''
        self.vfwebqq_inner = ''
        self.psession_id = ''
        self.client_id = 53999199
        self.msg_id = int(random.uniform(11111111, 88888888))

        # info
        self.self_info = None
        self.uin_map = {}
        self.group_map = {}
        pass

    # ----------------------------------------------------------------------------------------------------
    def login(self):
        # prepare login
        # ----------------------------------------------------------------------------------------------------
        # index page
        page_str = self.request.get(config['smart_qq_url'])
        # find login url
        login_url = self.get_page_info(page_str, r'\.src = "(.+?)"')
        page_str = self.request.get(login_url + '0')

        # appid
        appid = self.get_page_info(page_str, r'g_appid=encodeURIComponent\("(\d+)"\)')
        print("appid:", appid)
        # sign
        login_sig = self.get_page_info(page_str, r'g_login_sig=encodeURIComponent\("(.?)"\)')
        print("sign:", login_sig)
        # pt_version
        pt_version = self.get_page_info(page_str, r'g_pt_version=encodeURIComponent\("(\d+)"\)')
        print("pt_version:", pt_version)
        # mibao_css
        mibao_css = self.get_page_info(page_str, r'g_mibao_css=encodeURIComponent\("(.+?)"\)')
        print("mibao_css:", mibao_css)

        # login
        # ----------------------------------------------------------------------------------------------------
        start_time = self.get_current_time()
        # download QR
        self.request.download(config['qrcode_url'].format(appid), config['qrcode_path'])

        # verification
        while True:
            current_time = self.get_current_time()
            page_str = self.request.get(config['qrcode_login_url'].format(appid, current_time - start_time, mibao_css, pt_version, login_sig), Referer=login_url)
            print('qrcode:', page_str)
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

        # ptwebqq
        self.ptwebqq = self.request.get_cookie('ptwebqq')
        print('ptwebqq:', self.ptwebqq)

        # authorize
        while True:
            params = {
                'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(self.ptwebqq, self.client_id, self.psession_id),
            }
            page_str = self.request.post(config['qrcode_login2_url'], params, Referer=config['referer'])
            if page_str == '':
                time.sleep(2)
                continue
            print('authorize result:', page_str)
            result = json.loads(page_str)
            if result['retcode'] != 0:
                time.sleep(2)
                continue

            # success
            self.cip = result['result']['cip']
            self.vfwebqq = result['result']['vfwebqq']
            self.psession_id = result['result']['psessionid']
            print('login success')
            return True

    def process(self):
        self.get_vfwebqq()
        self.get_self_info()
        self.get_group_list()

        # loop
        while True:
            time.sleep(1)
            params = {
                'r': '{{"psessionid":"{0}","ptwebqq":"{1}","clientid":{2},"key":""}}'.format(self.psession_id, self.ptwebqq, self.client_id)
            }
            page_str = self.request.post(config['msg_url'], params, Referer=config['referer'])
            if page_str is None or page_str == '':
                time.sleep(config['handler_speed'])
                continue
            print('msg:', page_str)
            result = json.loads(page_str)

            # empty
            if result['retcode'] == 102:
                continue
            # update ptwebqq
            elif result['retcode'] == 116:
                self.ptwebqq = result['p']
                continue
            # msg
            elif result['retcode'] == 0:
                for result in result['result']:
                    msg_type = result['poll_type']
                    #if msg_type in NinjaHandle.__dict__:
                    #    NinjaHandle.__dict__[msg_type].__get__(self, NinjaHandle)(result)
            else:
                continue

    # receive
    # ----------------------------------------------------------------------------------------------------
    def message(self, msg):
        pass

    def sess_message(self, msg):
        pass

    def group_message(self, msg):
        self.robot.push_group_message(GroupMessage(self.group_map[msg['value']['from_uin']], msg))
        pass

    def discu_message(self, msg):
        pass

    def kick_message(self, msg):
        pass

    def buddies_status_change(self, msg):
        pass

    def input_notify(self, msg):
        pass

    def tips(self, msg):
        pass

    # send
    # ----------------------------------------------------------------------------------------------------
    def get_vfwebqq(self):
        page_str = self.request.get(config['get_vfwebqq_url'].format(self.ptwebqq, self.client_id, self.psession_id,self.get_current_time()), Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        print("get vfwebqq result:", result)
        if result['retcode'] != 0:
            return False
        result = result['result']
        self.vfwebqq_inner = result['vfwebqq']
        return True

    def get_self_info(self):
        page_str = self.request.get(config['get_self_info_url'].format(self.get_current_time()), Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        print("get self info result:", result)
        if result['retcode'] != 0:
            return False
        result = result['result']
        self.self_info = SelfInfo(result)
        return True

    def get_uin_info(self, uin):
        page_str = self.request.get(config['get_uin_info_url'].format(uin, self.vfwebqq), Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        print("get id info result:", result)
        if result['retcode'] != 0:
            return False
        self.uin_map[uin] = result['result']['account']
        return True

    def get_group_list(self):
        params = {
            'r': json.dumps({
                'vfwebqq': self.vfwebqq_inner,
                'hash': self.get_hash(self.uin, self.ptwebqq)
            })
        }
        page_str = self.request.post(config['get_group_list_url'], params, Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        print("get group list result:", result)
        if result['retcode'] != 0:
            return False
        # get info
        result = result['result']
        for group in result['gnamelist']:
            self.get_group_info(group['code'])
        return True

    def get_group_info(self, gcode):
        page_str = self.request.get(config['get_group_info_url'].format(gcode, self.vfwebqq_inner, self.get_current_time()), Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        print("get group info result:", result)
        if result['retcode'] != 0:
            return False
        # get info
        result = result['result']
        self.group_map[result['ginfo']['gid']] = GroupInfo(result)
        return True

    def send_to_group(self, uin, msg):
        msg.replace("\\", "\\\\")
        r_value = {
            "group_uin": uin,
            "content": '["{0}",["font",{{"name":"宋体","size":10,"style":[0,0,0],"color":"000000"}}]]'.format(msg),
            "face": 588,
            "clientid": self.client_id,
            "msg_id": self.msg_id,
            "psessionid": self.psession_id
        }
        params = {
            'r': json.dumps(r_value),
        }
        page_str = self.request.post(config['send_group_url'], params, Referer=config['referer'])
        if page_str == '':
            return False
        result = json.loads(page_str)
        print("send to group result:", result)
        if result['retcode'] != 0:
            return False
        self.msg_id += 1

    # tools
    # ----------------------------------------------------------------------------------------------------
    @staticmethod
    def get_current_time():
        return int(time.mktime(datetime.datetime.utcnow().timetuple())) * 1000

    @staticmethod
    def get_page_info(page, pattern):
        result = re.search(pattern, page)
        if result is None:
            return ''
        return result.group(1)

    @staticmethod
    def get_hash(uin, ptwebqq):
        uin = int(uin)
        n = [0, 0, 0, 0]
        for i in range(0, len(ptwebqq)):
            n[i % 4] ^= ord(ptwebqq[i]);
        u = ["EC", "OK"]
        v = []
        v.append(uin >> 24 & 255 ^ ord(u[0][0]))
        v.append(uin >> 16 & 255 ^ ord(u[0][1]))
        v.append(uin >> 8 & 255 ^ ord(u[1][0]))
        v.append(uin & 255 ^ ord(u[1][1]))
        u = []
        for i in range(0, 8):
            u.append(n[i >> 1] if i % 2 == 0 else v[i >> 1])
        n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        v = ""
        for i in range(0, len(u)):
            v += n[u[i] >> 4 & 15]
            v += n[u[i] & 15]
        return v


class SelfInfo(object):
    def __init__(self, msg):
        self.account = msg['account']
        self.allow = msg['allow']
        self.birthday = msg['birthday']
        self.blood = msg['blood']
        self.city = msg['city']
        self.college = msg['college']
        self.constel = msg['constel']
        self.country = msg['country']
        self.email = msg['email']
        self.face = msg['face']
        self.gender = msg['gender']
        self.homepage = msg['homepage']
        self.lnick = msg['lnick']
        self.mobile = msg['mobile']
        self.nick = msg['nick']
        self.occupation = msg['occupation']
        self.personal = msg['personal']
        self.phone = msg['phone']
        self.province = msg['province']
        self.shengxiao = msg['shengxiao']
        self.uin = msg['uin']
        self.vfwebqq = msg['vfwebqq']
        self.vip_info = msg['vip_info']


class GroupInfo(object):
    def __init__(self, msg):
        self.ginfo = msg['ginfo']
        self.minfo = msg['minfo']
        self.stats = msg['stats']
        self.vipinfo = msg['vipinfo']


class GroupMessage(object):
    def __init__(self, group_info, msg):
        self.group_info = group_info

        value = msg['value']
        self.msg_id = value['msg_id']
        self.from_uin = value['from_uin']
        self.to_uin = value['to_uin']
        self.msg_id2 = value['msg_id2']
        self.msg_type = value['msg_type']
        self.reply_ip = value['reply_ip']
        self.group_code = value['group_code']
        self.send_uin = value['send_uin']
        self.seq = value['seq']
        self.time = value['time']
        self.info_seq = value['info_seq']

        self.content = ''
        for content in value['content']:
            if isinstance(content, list):
                if content[0] == "font":
                    self.font = content
                elif content[0] == "face":
                    self.content += '[表情]'
                elif content[0] == "cface":
                    self.content += '[表情]'
                else:
                    self.content += '[Unknown]'
            else:
                self.content += content

