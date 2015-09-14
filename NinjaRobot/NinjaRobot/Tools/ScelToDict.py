import os
import sys
import struct

def scel_to_dict(file_path):
    for py_str, word_str in load_sogou_scel(file_path):
        pass

def load_sogou_scel(file_path):
    try:
        with open(file_path, 'rb') as fin:
            # common info
            file_size = os.path.getsize(file_path)
            chinese_offset = 0
            mask = read_byte(fin, 0x4, 0x1)
            if mask == 0x44:
                chinese_offset = 0x2628
            elif mask == 0x45:
                chinese_offset = 0x26C4
            else:
                raise StopIteration
            title = read_utf16(fin, 0x130, 0x338 - 0x130)
            type = read_utf16(fin, 0x338, 0x540 - 0x338)
            desc = read_utf16(fin, 0x540, 0xd40 - 0x540)
            samples = read_utf16(fin, 0xd40, 0x1540 - 0xd40)

            # get py map
            py_map = {}
            fin.seek(0x1540 + 4)
            while 1:
                py_code = struct.unpack('<H', fin.read(2))[0]
                py_len  = struct.unpack('<H', fin.read(2))[0]
                py_str  = read_utf16(fin, -1, py_len)
    
                if py_code not in py_map:
                    py_map[py_code] = py_str

                if py_str == 'zuo':
                    break

            # get chinese
            fin.seek(chinese_offset)
            while fin.tell() != file_size:
                chinese_count   = struct.unpack('<H', fin.read(2))[0]
                py_count = int(struct.unpack('<H', fin.read(2))[0] / 2)
    
                py_set = []
                for i in range(py_count):
                    py_id = struct.unpack('<H', fin.read(2))[0]
                    py_set.append(py_map[py_id])
                py_str = "'".join (py_set)

                for i in range(chinese_count):
                    chinese_len = struct.unpack('<H', fin.read(2))[0]
                    chinese_str = read_utf16(fin, -1, chinese_len)
                    fin.read(12)
                    yield py_str, chinese_str

    except Exception as e:
        print('error:', e)
        raise StopIteration

def read_byte(fin, offset=-1, len=1):
    if offset >= 0:
        fin.seek(offset)
    return fin.read(len)[0]

def read_utf16(fin, offset=-1, len=2):
    if offset >= 0:
        fin.seek(offset)
    str = fin.read(len)
    return str.decode('UTF-16LE')