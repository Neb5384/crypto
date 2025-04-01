import struct
def RSAMessage(msg, ask, s, n, e):
    """
    Message send with RSA encryption.
    :param msg: String
    :param ask: Type of interaction with the server
    :param s: Socket
    :param n: Quotient of the two premier number
    :param e: Public key
    :return: A message encode in RSA to the server
    """
    eMsg = RSAencode(msg, n, e)
    s.sendall(b"ISC" + ask.encode() + len(msg).to_bytes(2, byteorder="big") + eMsg)
    print(eMsg)

def sendMessage(msg, ask, s, encode, key):
    """
    Sending a message to a predefined server with a selected type of encryption.
    :param msg: String
    :param ask: Type of interaction with the server
    :param s: Socket
    :param encode: Type of encryption method
    :param key: Key used for the encryption
    :return: A message to the server
    """
    eMsg = ""
    match encode:
        case "none":
            eMsg = msg
            eMsg = encodeV2(eMsg)

        case "vigenere":
            eMsg = encodeVigenere(msg, key)

        case "shift":
            eMsg = shiftEncode(msg, key)

        case _:
            print("Can not encode")


    # Interaction with the server
    s.sendall(b"ISC" + ask.encode() + len(msg).to_bytes(2, byteorder="big") + eMsg)


def sendTask(leng, ask, s, encode, e_d):
    """
    Sending the first message to the server by sending the task we want to execute.
    :param leng: Length of the message to encode
    :param ask: Type of interaction with the server
    :param s: Socket
    :param encode: Type of encryption method
    :param e_d: Choice between encode/decode
    :return: A message from the server depending on the task asked
    """
    servmsg = "task " + encode +" "+ e_d +" "+ str(leng)
    s.sendall(b"ISC" + ask.encode() + len(servmsg).to_bytes(2, byteorder="big") + encodeV2(servmsg))

def cleanMsg(recv):
    r = recv.decode()
    rcvmessage = ""
    c = 0
    for i in r:
        if c >= 6:
            rcvmessage += i
        c += 1
    return rcvmessage.replace("\x00", "")
def encodeV2(msg):
    """
    Encode a string into an encode UTF-8 message.
    :param msg: String
    :return: UTF-8 message
    """
    uMsg = ""
    for i in msg:
        uLetter = i.encode("UTF-8")
        letter = (4-len(uLetter))* "\x00" + i
        uMsg += letter
    return uMsg.encode("UTF-8")


def shiftEncode(msg, key):
    """
    Encoding with the shift encryption method.
    :param msg: String
    :param key: The shift requested (Int)
    :return: The shifted message in bytes
    """
    out = b""
    for i in msg:
        iByte = encodeV2(i)
        ascii = (int.from_bytes(iByte,"big") + int(key)) % (2**32)
        out += ascii.to_bytes(4,"big")
    return out


def encodeVigenere(msg, key):
    """
    Encode the message with the Vigenere encryption method.
    :param msg: String
    :param key: The shift requested (String)
    :return: The shifted message in bytes
    """
    out = b""
    lmsg = list(msg)
    lkey = list(key)
    for i in range(len(msg)):
        j = i % len(lkey)
        charmsg = int.from_bytes(encodeV2(lmsg[i]),"big")
        charkey = int.from_bytes(encodeV2(lkey[j]),"big")
        newAscii = ((charmsg + charkey) % 2**32)
        out += newAscii.to_bytes(4,"big")
    return out

def decodeVigenere(msg, key):
    out = b""
    lmsg = list(msg)
    lkey = list(key)
    for i in range(len(msg)):
        j = i % len(lkey)
        charmsg = int.from_bytes(encodeV2(lmsg[i]),"big")
        charkey = int.from_bytes(encodeV2(lkey[j]),"big")
        newAscii = ((charmsg - charkey) % 2**32)
        out += newAscii.to_bytes(4,"big")
        print(out)
    return out

def RSAencode(msg, n , e):
    """
    Method that transform a given message to an RSA encode message
    :param msg: String
    :param n: Quotient of the two premier number
    :param e: Public key
    :return: Bytes encoded in RSA encryption
    """
    out = b""
    for i in msg:
        iByte = encodeV2(i)
        j = int.from_bytes(iByte,"big")
        val = pow(j, int(e), int(n))
        val2 = val % (2**32)
        out += val2.to_bytes(4, "big")
    return out

def RSA(msg, n, e):
    msg_bytes = encodeV2(msg)
    msg_int = int.from_bytes(msg_bytes, byteorder="big")

    enc_int = pow(msg_int, int(e), int(n))

    enc_bytes = enc_int.to_bytes(4, byteorder="big")

    return enc_bytes