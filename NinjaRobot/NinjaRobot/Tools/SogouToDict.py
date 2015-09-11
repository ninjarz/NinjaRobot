import os
import sys
import struct

def sogou_to_dict(file_path):
    pass

def load_sogou_scel(file_path):
    try:
        with open(file_path, 'r') as fin:
            file_size = os.path.getsize(file_path)
            title = read_utf16_str(fin, 0x130, 0x338 - 0x130)
            type = read_utf16_str(fin, 0x338, 0x540 - 0x338)
            desc = read_utf16_str(fin, 0x540, 0xd40 - 0x540)
            samples = read_utf16_str(fin, 0xd40, 0x1540 - 0xd40)

            hz_offset = 0
            fin.seek(0)
            mask = struct.unpack ('B', fin.read(128)[4])[0]
            if mask == 0x44:
                hz_offset = 0x2628
            elif mask == 0x45:
                hz_offset = 0x26C4
            else:
                sys.exit(1)

            py_map = {}
            fin.seek(0x1540 + 4)
            while 1:
                py_code = struct.unpack('<H', fin.read(2))[0]
                py_len  = struct.unpack('<H', fin.read(2))[0]
                py_str  = read_utf16_str(fin, -1, py_len)
    
                if py_code not in py_map:
                    py_map[py_code] = py_str
    
                if py_str == 'zuo':
                    break

            fin.seek(hz_offset)
            while fin.tell() != file_size:
                word_count   = struct.unpack('<H', fin.read(2))[0]
                pinyin_count = struct.unpack('<H', fin.read(2))[0] / 2
    
                py_set = []
                for i in range(pinyin_count):
                    py_id = struct.unpack('<H', fin.read(2))[0]
                    py_set.append(py_map[py_id])
                py_str = "'".join (py_set)

                for i in range(word_count):
                    word_len = struct.unpack('<H', fin.read(2))[0]
                    word_str = read_utf16_str(fin, -1, word_len)
                    f.read(12)
                    yield py_str, word_str
    except:
        return

def read_utf16_str(fin, offset=-1, len=2):
    if offset >= 0:
        fin.seek(offset)
    str = fin.read(len)
    return str.decode('UTF-16LE')