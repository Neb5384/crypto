import socket

import Key

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))

msg = "ABCDEF ouf enfin ça fonctionne pas ?=+*"



#def sendMessage(msg, ask, encoding, key)
def InteractionWithServer(leng,encode, e_d):

    Key.sendTask(leng, "s", s, encode, e_d)

    # Delete unecessary data
    recv1 = s.recv(1024)
    rcvmessage1 = Key.cleanMsg(recv1)
    l = rcvmessage1.split(" ")
    newKey = l[len(l)-1]

    recv2 = s.recv(1024)
    rcvmessage2 = Key.cleanMsg(recv2)

    print(rcvmessage1)
    print(rcvmessage2)


    Key.sendMessage(rcvmessage2 ,ask='s', s=s, encode=encode, key=newKey)

    rcvm = s.recv(1024)

    print(Key.cleanMsg(rcvm))

    rcvm = s.recv(1024)

    print(Key.cleanMsg(rcvm))





InteractionWithServer(40, encode = "shift",e_d = "encode")