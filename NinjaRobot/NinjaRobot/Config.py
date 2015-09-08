# default
config = {
    # data
    'dict_path': 'Data/Dict.txt',
    'reply_path': 'Data/Reply.json',
    'handler_speed': 0.1,
    'heart_speed': 0.1,

    # login
    'smart_qq_url': 'http://w.qq.com/login.html',
    'qrcode_url': 'https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=L&s=8&d=72&v=4',
    'qrcode_path': './qrcode.jpg',
    'qrcode_login_url': 'https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid={0}&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{1}&mibao_css={2}&t=undefined&g=1&js_type=0&js_ver={3}&login_sig={4}&pt_randsalt=0',
    'qrcode_login2_url': 'http://d.web2.qq.com/channel/login2',
    'referer': 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2',

    # msg
    'msg_url': 'http://d.web2.qq.com/channel/poll2',
    'get_vfwebqq': 'http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}',
    # user
    'get_self_info_url': 'http://s.web2.qq.com/api/get_self_info2?t={0}',
    'get_uin_info_url': 'http://s.web2.qq.com/api/get_friend_uin2?tuin={0}&type=1&vfwebqq={1}',
    # buddy
    'send_buddy_url': 'http://d.web2.qq.com/channel/send_buddy_msg2',
    # group
    'get_group_list_url': 'http://s.web2.qq.com/api/get_group_name_list_mask2',
    'get_group_info_url': 'http://s.web2.qq.com/api/get_group_info_ext2?gcode=413721552&vfwebqq=d4df9869b1b594f2875457edfacdcb58e4054416e9822125a3d42e7c296764f5576e9738a2e94ba8&t=1441526513605',
    'send_group_url': 'http://d.web2.qq.com/channel/send_qun_msg2',


}

def load_config():
    global config
    try:
        fin = open("Config", 'r')
        lines = fin.readlines()
        fin.close()
        for line in lines:
            words = line.split(' ')
            if type(config[words[0]]) is int:
                config[words[0]] = int(words[1])
            else:
                config[words[0]] = words[1]
    except:
        return