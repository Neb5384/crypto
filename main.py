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
    Discussion = ""

    # Sending the first message to the server
    Key.sendTask(leng, "s", s, encode, e_d)

    # Delete unnecessary data from the received messages
    recv1 = s.recv(1024)
    rcvmessage1 = Key.cleanMsg(recv1)
    print(rcvmessage1)
    Discussion += rcvmessage1 + "\n"

    recv2 = s.recv(1024)
    rcvmessage2 = Key.cleanMsg(recv2)
    print(rcvmessage2)
    Discussion += rcvmessage2 + "\n"

    # Turning rcvd message into an Array
    list = rcvmessage1.split(" ")

    # following interaction depending on the type of encryption
    rcvm = b""
    match encode:
        case "shift":
            newKey = list[len(list) - 1]
            Key.sendMessage(rcvmessage2, ask='s', s=s, encode=encode, key=newKey)

            rcvm = s.recv(len(rcvmessage1) * 1000)

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
    Discussion += Key.cleanMsg(rcvm) + "\n"
    return Discussion
