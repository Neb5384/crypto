import random
import socket


import Key

# Connecting to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))


def InteractionWithServer(leng, encode, e_d):
    """
    Main function used to communicate with the server.
    :param leng: Length of the received key
    :param encode: Method of encryption
    :param e_d: Choice between encode/decode
    :return: An interaction with the server
    """
    Conv = ""

    # Sending the first message to the server
    Key.sendTask(leng, "s", s, encode, e_d)

    # Delete unnecessary data from the received messages
    recv1 = s.recv(1024)
    rcvmessage1 = Key.cleanMsg(recv1)
    print(rcvmessage1)
    Conv += rcvmessage1 + "\n"

    recv2 = s.recv(1024)
    rcvmessage2 = Key.cleanMsg(recv2)
    print(rcvmessage2)
    Conv += rcvmessage2 + "\n"

    # Turning rcvd message into an Array
    list = rcvmessage1.split(" ")

    # following interaction depending on the type of encryption
    rcvm = b""
    match encode:
        case "shift":
            if e_d == "encode":
                newKey = list[len(list) - 1]
                Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

                rcvm = s.recv(len(rcvmessage1) * 1000)
            elif e_d == "decode":
                a = ""
            else: Conv = "Can't do this type of task"

        case "vigenere":
            newKey = list[len(list) - 1]
            Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

            rcvm = s.recv(len(rcvmessage2) * 1000)

            print(Key.cleanMsg(rcvm))

        case "RSA":
            # Key n
            keyn = list[len(list)-2]
            n = keyn.replace("n", "").replace("=", "").replace(",", "")

            # Key e
            keye = list[len(list) - 1]
            e = keye.replace("e", "").replace("=", "")

            # Send message with the encryption method
            Key.RSAMessage(rcvmessage2, ask='s',s=s, n=n, e=e)
            rcvm = s.recv(65000)

            print(Key.cleanMsg(rcvm))

        case _:
            pass
    Conv += Key.cleanMsg(rcvm) + "\n"
    return Conv

def InteractionWithServerShort(method):
    ask = "s"
    Conv = ""
    task = ""

    if method == "hash":
        method = "hash hash"
    elif method == "verify":
        method = "hash verify"
    else:
        method = "DifHel"


    servmsg = "task " + method
    s.sendall(b"ISC" + ask.encode() + len(servmsg).to_bytes(2, byteorder="big") + Key.encodeV2(servmsg))

    match method:
        case "hash":
            rcvm1 = s.recv(65000000)
            print(Key.cleanMsg(rcvm1))

            rcvm2 = s.recv(65000000)
            print(Key.cleanMsg(rcvm2))

            Key.sendMessage(rcvm2, "s", s, "hashing")
            rcvm = s.recv(65000000)
            print(Key.cleanMsg(rcvm))

        case "verify":
            rcvm1 = s.recv(65000000)
            print(Key.cleanMsg(rcvm1))

            rcvm2 = s.recv(65000000)
            print(Key.cleanMsg(rcvm2))

            Key.sendMessage(rcvm2, "s", s, "hashingVerify")

            rcvm3 = s.recv(650000)
            print(Key.cleanMsg(rcvm3))

        case "DifHel":
            rcvm1 = s.recv(65000000)
            print(Key.cleanMsg(rcvm1))

            P = Key.findP()
            G = Key.fingG(P)
            Keys = f"{P},{G}"
            Key.sendMessage(Keys, "s", s, "DifHel")

            rcvm2 = s.recv(65000000)
            print(Key.cleanMsg(rcvm2))

            rcvm3 = s.recv(650000)
            print(Key.cleanMsg(rcvm3))
            serverKey = int(Key.cleanMsg(rcvm3))

            a = random.randint(2, 10)
            msg = str(Key.publicKey(G, P, a))
            Key.sendMessage(msg,  "s", s, "DifHel")

            rcvm3 = s.recv(650000)
            print(Key.cleanMsg(rcvm3))
            msg = str(Key.sharedKey(P, a, serverKey))
            Key.sendMessage(msg, "s", s, "DifHel")

            rcvm3 = s.recv(650000)
            print(Key.cleanMsg(rcvm3))

InteractionWithServerShort("DifHel")

