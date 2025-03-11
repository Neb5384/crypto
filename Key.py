import struct


def sendMessage(msg, ask, s, encode, key):
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


def sendTask(leng,ask, s, encode,e_d):
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
#Encode the message
    uMsg = ""
    for i in msg:
        uLetter = i.encode("UTF-8")
        letter = (4-len(uLetter))* "\x00" + i
        uMsg += letter
    return uMsg.encode("UTF-8")


def shiftEncode(msg, key):
    out = b""
    for i in msg:
        iByte = encodeV2(i)
        ascii = (int.from_bytes(iByte,"big") + int(key)) % (2**32)
        out += ascii.to_bytes(4,"big")
    print(out)
    return out


def encodeVigenere(msg, key):
    out = ""
    lmsg = list(msg)
    lkey = list(key)
    for i in range(len(msg)):
        j = i % len(lkey)
        charmsg = ord(lmsg[i])
        charkey = ord(lkey[j])
        newAscii = ((charmsg + charkey) % 2**8)
        out += chr(newAscii)
    return out

def decodeVigenere(msg, key):
    out = ""
    lmsg = list(msg)
    lkey = list(key)
    for i in range(len(msg)):
        j = i % len(lkey)
        charmsg = ord(lmsg[i])
        charkey = ord(lkey[j])
        newAscii = ((charmsg - charkey) % 2**8)
        out += chr(newAscii)
    return out

