import random
import socket

import Key


# Connecting to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))
def yConv(msg):
    return f"You: {msg}" + "\n"

def sConv(msg):
    return f"Server: {msg}" + "\n"

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
    Conv += sConv(rcvmessage1)

    recv2 = s.recv(1024)
    rcvmessage2 = Key.cleanMsg(recv2)
    Conv += sConv(rcvmessage2)

    # Turning rcvd message into an Array
    list = rcvmessage1.split(" ")

    # following interaction depending on the type of encryption
    rcvm = b""
    match encode:
        case "shift":
            if e_d == "encode":
                newKey = list[len(list) - 1]
                Conv += Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

                rcvm = s.recv(len(rcvmessage1) * 1000)
            elif e_d == "decode":
                pass
            else: Conv = "Can't do this type of task"

        case "vigenere":
            newKey = list[len(list) - 1]
            Conv += Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

            rcvm = s.recv(len(rcvmessage2) * 1000)



        case "RSA":
            # Key n
            keyn = list[len(list)-2]
            n = keyn.replace("n", "").replace("=", "").replace(",", "")

            # Key e
            keye = list[len(list) - 1]
            e = keye.replace("e", "").replace("=", "")

            # Send message with the encryption method
            Conv += Key.RSAMessage(rcvmessage2, ask='s',s=s, n=n, e=e)
            rcvm = s.recv(65000)


        case _:
            pass
    Conv += sConv(Key.cleanMsg(rcvm))
    return Conv

def InteractionWithServerShort(method):
    '''
    Interaction with the server for hash and DifHel
    :param method: Choice of the encoding task (hash/verify/DifHel
    :return: Conversation with the server
    '''
    ask = "s"
    Conv = ""
    task = ""

    if method == "hash":
        task = "hash hash"
    elif method == "verify":
        task = "hash verify"
    else:
        task = "DifHel"


    servmsg = "task " + task
    Conv += yConv(servmsg)
    s.sendall(b"ISC" + ask.encode() + len(servmsg).to_bytes(2, byteorder="big") + Key.encodeV2(servmsg))
    print(Conv)

    match method:
        case "hash":
            print("yes")
            rcvm = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm)
            Conv += sConv(rcmessage)
            print(rcmessage)

            rcvm = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm)
            Conv += sConv(rcmessage)
            print(rcvm)


            Conv += Key.sendMessage(rcvm, "s", s, "hashing")
            #rcvm = s.recv(65000000)
            #rcmessage = Key.cleanMsg(rcvm)
            #Conv += rcmessage + "\n"

        case "verify":
            rcvm = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm)
            print(rcmessage)
            Conv += rcmessage + "\n"

            rcvm = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm)
            print(rcmessage)
            Conv += rcmessage + "\n"

            Conv += Key.sendMessage(rcvm, "s", s, "hashingVerify")

            #rcvm = s.recv(65000000)
            #rcmessage = Key.cleanMsg(rcvm)
            #Conv += rcmessage + "\n"

        case "DifHel":
            rcvm = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm)
            Conv += sConv(rcmessage)

            P = Key.findP()
            G = Key.fingG(P)
            Keys = f"{P},{G}"
            Conv += Key.sendMessage(Keys, "s", s, "DifHel")

            rcvm1 = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm1)
            Conv += sConv(rcmessage)

            rcvm2 = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm2)
            Conv += sConv(rcmessage)

            serverKey = int(Key.cleanMsg(rcvm2))
            a = random.randint(2, 10)
            msg = str(Key.publicKey(G, P, a))
            Conv += Key.sendMessage(msg, "s", s, "DifHel")


            rcvm3 = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm3)
            Conv += sConv(rcmessage)

            msg = str(Key.sharedKey(P, a, serverKey))
            Conv += Key.sendMessage(msg, "s", s, "DifHel")

            rcvm5 = s.recv(65000000)
            rcmessage = Key.cleanMsg(rcvm5)
            Conv += sConv(rcmessage)

        case _: pass
    return Conv


