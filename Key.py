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

