
def SendMessage(msg, Key, ask, s):
    uMsg = Key.shiftEncode(msg, 1)
    uMsg = Key.encodeV2(uMsg)
    # Interaction with the server
    s.sendall(b"ISC" + Key.encodeV2(ask) + len(msg).to_bytes(2, byteorder="big") + uMsg)

def ReceiveMessage(s):
    recv = s.recv(1024)
    r = recv.decode()

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
        charmsg = ord(lmsg[i])
        charkey = ord(lkey[j])
        newAscii = ((charmsg + charkey) % 8**8)
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
        newAscii = ((charmsg - charkey) % 8**8)
        out += chr(newAscii)
    return out


msg = "testabc testabc testabc testabc testabc"
key = "ABC"

newmsg = encodeVigenere(msg,key)
print(newmsg)

print(decodeVigenere(newmsg,key))
