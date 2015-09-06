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

print(get_hash('3264630074', '47f2f86d964a2a5e4ea9a9c238013cc91d7c10e43f9e4665f1abab55b8e9639d'))