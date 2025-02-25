import socket

import Key

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))

msg = "ABCDEF ouf enfin ça fonctionne pas ?=+*"




def sendMessage(msg, ask, encoding, direction):
    if ask == 't' or 's' or 'i':
        ask = ask
    else : print("request unavailable")


    #uMsg = Key.encodeV2(msg)
    uMsg = Key.shiftEncode(msg, 1)
    uMsg = Key.encodeV2(uMsg)
    # Interaction with the server
    s.sendall(b"ISC"+ ask + len(msg).to_bytes(2, byteorder="big") + uMsg)
    recv = s.recv(1024)
    r = recv.decode()


    # Delete unecessary data
    rcvmessage = ""
    c = 0
    for i in r :
        if c >= 6 :
            rcvmessage += i
        c += 1
    print(rcvmessage.replace("\x00", ""))


sendMessage(msg)