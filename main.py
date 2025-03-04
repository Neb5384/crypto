import socket

import Key

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))

msg = "ABCDEF ouf enfin ça fonctionne pas ?=+*"



#def sendMessage(msg, ask, encoding, key)
def InteractionWithServer(msg, ask, encode, e_d, key):
    if ask != 't' or ask != 's' or ask != 'i':
        print(ask[0])



    #uMsg = Key.encodeV2(msg)
    if ask == 't':
        Key.sendMessage(msg, ask, s, encode,e_d, key)
    elif ask == 's' :
        Key.sendS(msg, ask, s, encode,e_d)

    # Delete unecessary data
    recv = s.recv(1024)
    r = recv.decode()
    rcvmessage = ""
    c = 0
    for i in r:
        if c >= 6:
            rcvmessage += i
        c += 1
    print(rcvmessage.replace("\x00", ""))


InteractionWithServer(msg,ask = 's', encode = "vigenere",e_d = "encode", key="WATER")
InteractionWithServer(msg,ask = 't', encode="none",e_d = "decode", key="WATER")