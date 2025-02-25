import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("vlbelintrocrypto.hevs.ch", 6000))

msg = "AB ❤"

uMsg = ""
for i in msg:
    uLetter = i.encode("UTF-8")
    letter = (4-len(uLetter))* "0" + i
    uMsg += letter
uMsg = uMsg.encode("UTF-8")

print(b"ISCt\x00\x04"+uMsg)

s.sendall(b"ISCt\x00\x04"+uMsg)
recv = s.recv(1024)
print(recv)



