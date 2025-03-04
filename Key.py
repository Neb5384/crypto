
def sendMessage(msg, ask, s, encode,e_d, key):
    eMsg = ""
    match encode:
        case "none":
            eMsg = msg
        case "vigenere":
            eMsg = encodeVigenere(msg, key)
        case "Shift":
            eMsg = shiftEncode(msg, key)
        case _:
            print("Can not encode")


    # Interaction with the server

    uMsg = encodeV2(eMsg)
    s.sendall(b"ISC" + ask.encode() + len(msg).to_bytes(2, byteorder="big") + uMsg)


def sendS(msg, ask, s, encode,e_d):
    servmsg = "task " + encode +" "+ e_d +" "+ str(len(msg))
    s.sendall(b"ISC" + ask.encode() + len(servmsg).to_bytes(2, byteorder="big") + encodeV2(servmsg))


def encodeV2(msg):
#Encode the message
    uMsg = ""
    for i in msg:
        uLetter = i.encode("UTF-8")
        letter = (4-len(uLetter))* "\x00" + i
        uMsg += letter
    return uMsg.encode("UTF-8")


def shiftEncode(msg, key):
    out = ""
    for i in msg:
        ascii = ord(i) + key
        out += chr(ascii)
    return out

def encodeVigenere(msg, key):
    out = ""
    lmsg = list(msg)
    lkey = list(key)
    for i in range(len(msg)):
        j = i % len(lkey)
        charmsg = ord(lmsg[i]) - ord('A')
        charkey = ord(lkey[j]) - ord('A')
        newAscii = ((charmsg + charkey) % 26) + ord('A')
        out += chr(newAscii)
    return out


"""uMsg = Key.encodeV2(uMsg)
    # Interaction with the server
    s.sendall(b"ISC" + Key.encodeV2(ask) + len(msg).to_bytes(2, byteorder="big") + uMsg)
    recv = s.recv(1024)
    r = recv.decode()"""

