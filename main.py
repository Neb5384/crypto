import socket


import Key

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))

msg = "ABCDEF ouf enfin ça fonctionne pas ?=+*"




#def sendMessage(msg, ask, encoding, key)
def InteractionWithServer(leng, encode, e_d):
    log = ""

    Key.sendTask(leng, "s", s, encode, e_d)

    # Delete unecessary data
    recv1 = s.recv(1024)
    rcvmessage1 = Key.cleanMsg(recv1)
    print(rcvmessage1)
    log += rcvmessage1 + "\n"


    recv2 = s.recv(1024)
    rcvmessage2 = Key.cleanMsg(recv2)
    print(rcvmessage2)
    log += rcvmessage2 + "\n"


    l = rcvmessage1.split(" ")
    match encode:
        case "shift":
            newKey = l[len(l) - 1]
            Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

            rcvm = s.recv(1024)






        case "vigenere":
            newKey = l[len(l) - 1]
            Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

            rcvm = s.recv(1024)

            print(Key.cleanMsg(rcvm))



        case "RSA":
            keyn = l[len(l)-2]
            keye = l[len(l)-1]
            e = keye.replace("e", "").replace("=", "")
            n = keyn.replace("n", "").replace("=", "").replace(",", "")
            Key.RSAMessage(rcvmessage2, ask='s',s=s, n=n, e=e)
            rcvm = s.recv(1024)

            print(Key.cleanMsg(rcvm))

        case _ :
            pass


    log += Key.cleanMsg(rcvm) + "\n"
    return log
