import struct
import random


fc = 0x01
value = 'stop'
unit_id = 1

f_body = struct.pack('B', fc) + str.encode(str(value), encoding='utf-8')
body_l = len(f_body)
f_body += str.encode(str(value), encoding='utf-8')
print(body_l)
print(f_body)

a = 1.00002
b = str.encode(str(a), encoding='utf-8')
c = bytes.decode(b, encoding='utf-8')
d = float(c)
"""
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f_body)
    data = s.recv(1024)
"""

print(struct.unpack('B', f_body[0:1])[0])
print(bytes.decode(f_body[1:body_l], encoding='utf-8'))